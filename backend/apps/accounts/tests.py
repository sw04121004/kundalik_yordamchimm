from unittest.mock import patch, MagicMock

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from apps.ai.models import Conversation, Message
from apps.planner.models import Task
from apps.services.models import Category, Favorite, Service, Transaction, UsageLog
from apps.accounts.throttles import LoginThrottle, PasswordChangeThrottle, RegisterThrottle
from apps.accounts.models import PasswordResetCode
import re

User = get_user_model()


class AccountAPITests(APITestCase):
	def setUp(self):
		cache.clear()
		self.user = User.objects.create_user(
			username="audit-user",
			email="audit@example.com",
			password="StrongPass123!",
			first_name="Audit",
		)

	def test_registration_creates_hashed_password_and_tokens(self):
		response = self.client.post(
			reverse("register"),
			{
				"username": "new-user",
				"email": "new@example.com",
				"password": "StrongPass123!",
				"password2": "StrongPass123!",
			},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		created_user = User.objects.get(username="new-user")
		self.assertTrue(created_user.check_password("StrongPass123!"))
		self.assertNotEqual(created_user.password, "StrongPass123!")
		self.assertIn("access", response.data)
		self.assertIn("refresh", response.data)

	def test_registration_rejects_mismatched_passwords(self):
		response = self.client.post(
			reverse("register"),
			{
				"username": "new-user",
				"password": "StrongPass123!",
				"password2": "DifferentPass123!",
			},
			format="json",
		)

	def test_registration_rejects_duplicate_username_and_localizes_error(self):
		# Default (uz)
		response_uz = self.client.post(
			reverse("register"),
			{
				"username": self.user.username,
				"password": "StrongPass123!",
				"password2": "StrongPass123!",
			},
			format="json",
			HTTP_ACCEPT_LANGUAGE="uz",
		)
		self.assertEqual(response_uz.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn("allaqachon band", " ".join(response_uz.data["username"]))
		self.assertNotIn("A user with that username already exists", " ".join(response_uz.data["username"]))

		# Russian (ru)
		response_ru = self.client.post(
			reverse("register"),
			{
				"username": self.user.username,
				"password": "StrongPass123!",
				"password2": "StrongPass123!",
			},
			format="json",
			HTTP_ACCEPT_LANGUAGE="ru",
		)
		self.assertEqual(response_ru.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn("уже существует", " ".join(response_ru.data["username"]))
		self.assertNotIn("A user with that username already exists", " ".join(response_ru.data["username"]))

	def test_registration_enforces_eight_character_password_and_localizes_error(self):
		response = self.client.post(
			reverse("register"),
			{"username": "short-pass", "password": "short7!", "password2": "short7!"},
			format="json",
			HTTP_ACCEPT_LANGUAGE="ru",
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn("8 символов", " ".join(response.data["password"]))
		self.assertFalse(User.objects.filter(username="short-pass").exists())

	def test_authentication_and_password_endpoints_are_throttled(self):
		login_rates = {**LoginThrottle.THROTTLE_RATES, "auth_login": "1/min"}
		register_rates = {**RegisterThrottle.THROTTLE_RATES, "auth_register": "1/min"}
		password_rates = {**PasswordChangeThrottle.THROTTLE_RATES, "auth_password_change": "1/min"}
		with patch.object(LoginThrottle, "THROTTLE_RATES", login_rates), patch.object(RegisterThrottle, "THROTTLE_RATES", register_rates), patch.object(PasswordChangeThrottle, "THROTTLE_RATES", password_rates):
			cache.clear()
			login_payload = {"username": self.user.username, "password": "StrongPass123!"}
			self.assertEqual(self.client.post(reverse("login"), login_payload, format="json").status_code, status.HTTP_200_OK)
			self.assertEqual(self.client.post(reverse("login"), login_payload, format="json").status_code, status.HTTP_429_TOO_MANY_REQUESTS)

			cache.clear()
			register_payload = {"username": "throttle-user", "password": "StrongPass123!", "password2": "StrongPass123!"}
			self.assertEqual(self.client.post(reverse("register"), register_payload, format="json").status_code, status.HTTP_201_CREATED)
			register_payload["username"] = "another-throttle-user"
			self.assertEqual(self.client.post(reverse("register"), register_payload, format="json").status_code, status.HTTP_429_TOO_MANY_REQUESTS)

			cache.clear()
			self.client.force_authenticate(self.user)
			password_payload = {"old_password": "StrongPass123!", "new_password": "NewStrongPass123!", "new_password2": "NewStrongPass123!"}
			self.assertEqual(self.client.post(reverse("change-password"), password_payload, format="json").status_code, status.HTTP_200_OK)
			self.assertEqual(self.client.post(reverse("change-password"), password_payload, format="json").status_code, status.HTTP_429_TOO_MANY_REQUESTS)

	def test_login_accepts_username_or_email_in_username_field(self):
		for login_value in (self.user.username, self.user.email):
			with self.subTest(login_value=login_value):
				response = self.client.post(
					reverse("login"),
					{"username": login_value, "password": "StrongPass123!"},
					format="json",
				)
				self.assertEqual(response.status_code, status.HTTP_200_OK)
				self.assertIn("access", response.data)
				self.assertIn("refresh", response.data)

	def test_profile_requires_authentication_and_is_user_scoped(self):
		url = reverse("me")
		self.assertEqual(self.client.get(url).status_code, status.HTTP_401_UNAUTHORIZED)

		self.client.force_authenticate(self.user)
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["username"], self.user.username)

		response = self.client.patch(url, {"first_name": "Updated"}, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.user.refresh_from_db()
		self.assertEqual(self.user.first_name, "Updated")

	def test_password_change_validates_old_password_and_updates_hash(self):
		self.client.force_authenticate(self.user)
		url = reverse("change-password")
		response = self.client.post(
			url,
			{
				"old_password": "wrong-password",
				"new_password": "NewStrongPass123!",
				"new_password2": "NewStrongPass123!",
			},
			format="json",
		)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		response = self.client.post(
			url,
			{
				"old_password": "StrongPass123!",
				"new_password": "NewStrongPass123!",
				"new_password2": "NewStrongPass123!",
			},
			format="json",
		)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password("NewStrongPass123!"))

	def test_refresh_endpoint_returns_new_access_token(self):
		login = self.client.post(
			reverse("login"),
			{"username": self.user.username, "password": "StrongPass123!"},
			format="json",
		)
		response = self.client.post(
			reverse("token_refresh"), {"refresh": login.data["refresh"]}, format="json"
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn("access", response.data)
		self.assertIn("refresh", response.data)
		# Old refresh is now blacklisted after rotation
		old_reuse = self.client.post(
			reverse("token_refresh"), {"refresh": login.data["refresh"]}, format="json"
		)
		self.assertEqual(old_reuse.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_logout_blacklists_only_the_authenticated_users_refresh_token(self):
		other_user = User.objects.create_user(username="other-audit-user", password="StrongPass123!")
		own_refresh = RefreshToken.for_user(self.user)
		other_refresh = RefreshToken.for_user(other_user)
		url = reverse("logout")

		self.assertEqual(self.client.post(url, {"refresh": str(own_refresh)}, format="json").status_code, status.HTTP_401_UNAUTHORIZED)
		self.client.force_authenticate(self.user)
		wrong_owner = self.client.post(url, {"refresh": str(other_refresh)}, format="json")
		self.assertEqual(wrong_owner.status_code, status.HTTP_403_FORBIDDEN)

		response = self.client.post(url, {"refresh": str(own_refresh)}, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(
			self.client.post(reverse("token_refresh"), {"refresh": str(own_refresh)}, format="json").status_code,
			status.HTTP_401_UNAUTHORIZED,
		)
		self.assertEqual(
			self.client.post(reverse("token_refresh"), {"refresh": str(other_refresh)}, format="json").status_code,
			status.HTTP_200_OK,
		)

	def test_untracked_preexisting_refresh_token_remains_valid(self):
		refresh = RefreshToken.for_user(self.user)
		OutstandingToken.objects.filter(jti=refresh["jti"]).delete()

		response = self.client.post(reverse("token_refresh"), {"refresh": str(refresh)}, format="json")

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn("access", response.data)

	def test_account_deletion_requires_password_and_cascades_only_own_data(self):
		other_user = User.objects.create_user(username="other-delete-user", password="StrongPass123!")
		category = Category.objects.create(name="Test", slug="delete-account-test")
		service = Service.objects.create(category=category, name="Test", slug="delete-account-test", route="/test")
		own_task = Task.objects.create(user=self.user, title="Own task")
		other_task = Task.objects.create(user=other_user, title="Other task")
		own_conversation = Conversation.objects.create(user=self.user, title="Own chat")
		other_conversation = Conversation.objects.create(user=other_user, title="Other chat")
		own_message = Message.objects.create(conversation=own_conversation, role="user", content="Own message")
		other_message = Message.objects.create(conversation=other_conversation, role="user", content="Other message")
		own_transaction = Transaction.objects.create(
			user=self.user, type="expense", amount="10.00", category="food", date="2026-11-09",
		)
		other_transaction = Transaction.objects.create(
			user=other_user, type="expense", amount="20.00", category="food", date="2026-11-09",
		)
		own_favorite = Favorite.objects.create(user=self.user, service=service)
		other_favorite = Favorite.objects.create(user=other_user, service=service)
		own_usage = UsageLog.objects.create(user=self.user, service=service)
		other_usage = UsageLog.objects.create(user=other_user, service=service)
		refresh = RefreshToken.for_user(self.user)
		url = reverse("account-delete")
		self.assertEqual(self.client.delete(url, format="json").status_code, status.HTTP_401_UNAUTHORIZED)
		self.client.force_authenticate(self.user)
		missing_password = self.client.delete(url, {}, format="json")
		self.assertEqual(missing_password.status_code, status.HTTP_400_BAD_REQUEST)

		bad_password = self.client.delete(url, {"current_password": "wrong-password"}, format="json")
		self.assertEqual(bad_password.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertTrue(User.objects.filter(pk=self.user.pk).exists())
		self.assertTrue(Task.objects.filter(pk=own_task.pk).exists())
		self.assertTrue(Conversation.objects.filter(pk=own_conversation.pk).exists())
		self.assertTrue(Message.objects.filter(pk=own_message.pk).exists())
		self.assertTrue(Transaction.objects.filter(pk=own_transaction.pk).exists())
		self.assertTrue(Favorite.objects.filter(pk=own_favorite.pk).exists())
		self.assertTrue(UsageLog.objects.filter(pk=own_usage.pk).exists())

		response = self.client.delete(url, {"current_password": "StrongPass123!"}, format="json")
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(User.objects.filter(pk=self.user.pk).exists())
		self.assertFalse(Task.objects.filter(user_id=self.user.pk).exists())
		self.assertFalse(Conversation.objects.filter(user_id=self.user.pk).exists())
		self.assertFalse(Message.objects.filter(conversation_id=own_conversation.pk).exists())
		self.assertFalse(Transaction.objects.filter(user_id=self.user.pk).exists())
		self.assertFalse(Favorite.objects.filter(user_id=self.user.pk).exists())
		self.assertFalse(UsageLog.objects.filter(user_id=self.user.pk).exists())
		self.assertTrue(User.objects.filter(pk=other_user.pk).exists())
		self.assertTrue(Task.objects.filter(pk=other_task.pk, user=other_user).exists())
		self.assertTrue(Conversation.objects.filter(pk=other_conversation.pk, user=other_user).exists())
		self.assertTrue(Message.objects.filter(pk=other_message.pk, conversation=other_conversation).exists())
		self.assertTrue(Transaction.objects.filter(pk=other_transaction.pk, user=other_user).exists())
		self.assertTrue(Favorite.objects.filter(pk=other_favorite.pk, user=other_user).exists())
		self.assertTrue(UsageLog.objects.filter(pk=other_usage.pk, user=other_user).exists())
		self.assertEqual(
			self.client.post(reverse("token_refresh"), {"refresh": str(refresh)}, format="json").status_code,
			status.HTTP_401_UNAUTHORIZED,
		)

	def test_account_deletion_confirmation_normalization(self):
		url = reverse("account-delete")
		# 1. Noto'g'ri tasdiqlash so'zi rad etiladi
		self.client.force_authenticate(self.user)
		res = self.client.delete(url, {"current_password": "StrongPass123!", "confirmation": "bekor-qil"}, format="json")
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn("confirmation", res.data)
		self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

		# 2. Noto'g'ri parol bo'lsa rad etiladi
		res_bad_pw = self.client.delete(url, {"current_password": "wrong-password", "confirmation": "o'chirish"}, format="json")
		self.assertEqual(res_bad_pw.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn("current_password", res_bad_pw.data)
		self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

		# 3. Har xil apostrof turlari va uchala til so'zi (uz/ru/en) qabul qilinadi
		confirmation_variants = [
			"o'chirish",
			"O'chirish",
			"o’chirish",
			"Oʻchirish",
			"oʼchirish",
			"O‘chirish",
			"ochirish",
			"Delete",
			"delete",
			"Удалить",
			"удалить",
		]
		for idx, word in enumerate(confirmation_variants):
			u = User.objects.create_user(username=f"del-var-{idx}", password="StrongPass123!")
			self.client.force_authenticate(u)
			resp = self.client.delete(url, {"current_password": "StrongPass123!", "confirmation": word}, format="json")
			self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
			self.assertFalse(User.objects.filter(pk=u.pk).exists())

	@override_settings(EMAIL_PROVIDER="smtp", EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
	@patch("apps.accounts.views.send_mail")
	def test_email_password_reset_code_is_hashed_one_time_and_changes_password(self, send_mail_mock):
		request = self.client.post(reverse("password-reset-request"), {"email": self.user.email}, format="json")
		self.assertEqual(request.status_code, status.HTTP_202_ACCEPTED)
		code = re.search(r"\b(\d{6})\b", send_mail_mock.call_args.args[1]).group(1)
		reset = PasswordResetCode.objects.get(user=self.user)
		self.assertNotEqual(reset.code_hash, code)

		payload = {"email": self.user.email, "code": code, "new_password": "UpdatedPass456!", "new_password2": "UpdatedPass456!"}
		confirmed = self.client.post(reverse("password-reset-confirm"), payload, format="json")
		self.assertEqual(confirmed.status_code, status.HTTP_200_OK)
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password("UpdatedPass456!"))
		login = self.client.post(reverse("login"), {"username": self.user.email, "password": "UpdatedPass456!"}, format="json")
		self.assertEqual(login.status_code, status.HTTP_200_OK)
		self.assertIsNotNone(PasswordResetCode.objects.get(pk=reset.pk).used_at)
		self.assertEqual(self.client.post(reverse("password-reset-confirm"), payload, format="json").status_code, status.HTTP_400_BAD_REQUEST)

	@override_settings(EMAIL_PROVIDER="smtp", EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
	def test_password_reset_does_not_disclose_unknown_email(self):
		known = self.client.post(reverse("password-reset-request"), {"email": self.user.email}, format="json")
		unknown = self.client.post(reverse("password-reset-request"), {"email": "missing@example.com"}, format="json")
		self.assertEqual(known.status_code, unknown.status_code)
		self.assertEqual(known.data["detail"], unknown.data["detail"])

	@override_settings(EMAIL_PROVIDER="brevo", BREVO_API_KEY="")
	def test_password_reset_unconfigured_returns_503(self):
		res_uz = self.client.post(reverse("password-reset-request"), {"email": self.user.email}, format="json", HTTP_ACCEPT_LANGUAGE="uz")
		self.assertEqual(res_uz.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
		self.assertIn("Email yuborish sozlanmagan", res_uz.data["detail"])

		cache.clear()
		res_ru = self.client.post(reverse("password-reset-request"), {"email": "missing@example.com"}, format="json", HTTP_ACCEPT_LANGUAGE="ru")
		self.assertEqual(res_ru.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
		self.assertIn("Отправка email не настроена", res_ru.data["detail"])

		cache.clear()
		res_en = self.client.post(reverse("password-reset-request"), {"email": self.user.email}, format="json", HTTP_ACCEPT_LANGUAGE="en")
		self.assertEqual(res_en.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
		self.assertIn("Email sending is not configured", res_en.data["detail"])

	@override_settings(EMAIL_PROVIDER="brevo", BREVO_API_KEY="test-brevo-key-123", EMAIL_FROM="noreply@qulay.uz", EMAIL_FROM_NAME="Qulay.uz")
	@patch("apps.accounts.views.requests.post")
	def test_password_reset_sends_via_brevo_api(self, mock_post):
		mock_response = MagicMock()
		mock_response.status_code = 201
		mock_post.return_value = mock_response

		res = self.client.post(reverse("password-reset-request"), {"email": self.user.email}, format="json", HTTP_ACCEPT_LANGUAGE="uz")
		self.assertEqual(res.status_code, status.HTTP_202_ACCEPTED)
		self.assertEqual(res.data["detail"], "Agar email akkauntga tegishli bo'lsa, tiklash kodi yuborildi.")

		mock_post.assert_called_once()
		call_kwargs = mock_post.call_args.kwargs
		self.assertEqual(call_kwargs["headers"]["api-key"], "test-brevo-key-123")
		self.assertEqual(call_kwargs["json"]["to"], [{"email": self.user.email}])
		self.assertIn("Qulay.uz", call_kwargs["json"]["subject"])

	@override_settings(EMAIL_PROVIDER="brevo", BREVO_API_KEY="test-brevo-key-123")
	@patch("apps.accounts.views.requests.post")
	def test_password_reset_brevo_failure_gracefully_returns_202(self, mock_post):
		mock_post.side_effect = Exception("Brevo connection failed")

		res = self.client.post(reverse("password-reset-request"), {"email": self.user.email}, format="json")
		self.assertEqual(res.status_code, status.HTTP_202_ACCEPTED)
		self.assertEqual(res.data["detail"], "Agar email akkauntga tegishli bo'lsa, tiklash kodi yuborildi.")

	def test_login_with_duplicate_email_matches_correct_user_by_password(self):
		dup_email = "duplicate@example.com"
		u1 = User.objects.create_user(username="dup-user-1", email=dup_email, password="PassOne123!")
		u2 = User.objects.create_user(username="dup-user-2", email=dup_email, password="PassTwo456!")

		# Email + PassOne123! kirilganda dup-user-1 tanlanadi
		res1 = self.client.post(reverse("login"), {"username": dup_email, "password": "PassOne123!"}, format="json")
		self.assertEqual(res1.status_code, status.HTTP_200_OK)
		token1 = RefreshToken(res1.data["refresh"])
		self.assertEqual(token1["username"], "dup-user-1")

		# Email + PassTwo456! kirilganda dup-user-2 tanlanadi
		res2 = self.client.post(reverse("login"), {"username": dup_email, "password": "PassTwo456!"}, format="json")
		self.assertEqual(res2.status_code, status.HTTP_200_OK)
		token2 = RefreshToken(res2.data["refresh"])
		self.assertEqual(token2["username"], "dup-user-2")

		# Email + noto'g'ri parol bo'lsa 401
		res_bad = self.client.post(reverse("login"), {"username": dup_email, "password": "WrongPass999!"}, format="json")
		self.assertEqual(res_bad.status_code, status.HTTP_401_UNAUTHORIZED)

		# Username orqali kirish: faqat o'sha username ga tegishli parol bilan kiradi
		res_u1_good = self.client.post(reverse("login"), {"username": "dup-user-1", "password": "PassOne123!"}, format="json")
		self.assertEqual(res_u1_good.status_code, status.HTTP_200_OK)
		res_u1_wrong = self.client.post(reverse("login"), {"username": "dup-user-1", "password": "PassTwo456!"}, format="json")
		self.assertEqual(res_u1_wrong.status_code, status.HTTP_401_UNAUTHORIZED)

	@override_settings(EMAIL_PROVIDER="smtp", EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
	@patch("apps.accounts.views.send_mail")
	def test_password_reset_and_change_blacklists_tokens_and_enforces_new_password(self, send_mail_mock):
		user = User.objects.create_user(username="reset-user", email="resetme@example.com", password="InitialPass123!")
		old_refresh = RefreshToken.for_user(user)

		# 1. Reset code so'rash
		req = self.client.post(reverse("password-reset-request"), {"email": user.email}, format="json")
		self.assertEqual(req.status_code, status.HTTP_202_ACCEPTED)
		code = re.search(r"\b(\d{6})\b", send_mail_mock.call_args.args[1]).group(1)

		# 2. Reset confirm
		confirm_payload = {
			"email": user.email,
			"code": code,
			"new_password": "BrandNewPass789!",
			"new_password2": "BrandNewPass789!",
		}
		confirm_res = self.client.post(reverse("password-reset-confirm"), confirm_payload, format="json")
		self.assertEqual(confirm_res.status_code, status.HTTP_200_OK)

		# 3. Eski parol rad etilishi kerak (username va email bilan)
		bad_login_username = self.client.post(reverse("login"), {"username": user.username, "password": "InitialPass123!"}, format="json")
		self.assertEqual(bad_login_username.status_code, status.HTTP_401_UNAUTHORIZED)
		bad_login_email = self.client.post(reverse("login"), {"username": user.email, "password": "InitialPass123!"}, format="json")
		self.assertEqual(bad_login_email.status_code, status.HTTP_401_UNAUTHORIZED)

		# 4. Yangi parol muvaffaqiyatli kirishi kerak (username va email bilan)
		good_login_username = self.client.post(reverse("login"), {"username": user.username, "password": "BrandNewPass789!"}, format="json")
		self.assertEqual(good_login_username.status_code, status.HTTP_200_OK)
		good_login_email = self.client.post(reverse("login"), {"username": user.email, "password": "BrandNewPass789!"}, format="json")
		self.assertEqual(good_login_email.status_code, status.HTTP_200_OK)

		# 5. Paroldan oldingi eski refresh token blacklist bo'lgan
		refresh_attempt = self.client.post(reverse("token_refresh"), {"refresh": str(old_refresh)}, format="json")
		self.assertEqual(refresh_attempt.status_code, status.HTTP_401_UNAUTHORIZED)

		# 6. Change-password tekshiruvi:
		user.refresh_from_db()
		active_refresh = RefreshToken(good_login_username.data["refresh"])
		self.client.force_authenticate(user)
		change_res = self.client.post(
			reverse("change-password"),
			{"old_password": "BrandNewPass789!", "new_password": "ThirdPass1234!", "new_password2": "ThirdPass1234!"},
			format="json",
		)
		self.assertEqual(change_res.status_code, status.HTTP_200_OK)

		# Change passworddan keyin oldingi token blacklist bo'lishi kerak
		self.client.force_authenticate(None)
		refresh_attempt2 = self.client.post(reverse("token_refresh"), {"refresh": str(active_refresh)}, format="json")
		self.assertEqual(refresh_attempt2.status_code, status.HTTP_401_UNAUTHORIZED)

		# Yangi "ThirdPass1234!" bilan login o'tadi
		final_login = self.client.post(reverse("login"), {"username": user.email, "password": "ThirdPass1234!"}, format="json")
		self.assertEqual(final_login.status_code, status.HTTP_200_OK)

	def test_registration_rejects_duplicate_email_case_insensitively(self):
		res = self.client.post(
			reverse("register"),
			{
				"username": "distinct-username",
				"email": self.user.email.upper(),  # AUDIT@EXAMPLE.COM
				"password": "StrongPass123!",
				"password2": "StrongPass123!",
			},
			format="json",
			HTTP_ACCEPT_LANGUAGE="uz",
		)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertIn("allaqachon", " ".join(res.data["email"]))
