from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

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
