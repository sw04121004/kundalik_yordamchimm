from unittest.mock import patch

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

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertFalse(User.objects.filter(username="new-user").exists())

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

	@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
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

	@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
	def test_password_reset_does_not_disclose_unknown_email(self):
		known = self.client.post(reverse("password-reset-request"), {"email": self.user.email}, format="json")
		unknown = self.client.post(reverse("password-reset-request"), {"email": "missing@example.com"}, format="json")
		self.assertEqual(known.status_code, unknown.status_code)
		self.assertEqual(known.data["detail"], unknown.data["detail"])
