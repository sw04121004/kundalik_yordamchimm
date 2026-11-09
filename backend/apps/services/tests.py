from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone

from .models import Category, Favorite, Service, Transaction

User = get_user_model()


class ServicesAPITests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="service-user", password="StrongPass123!")
		self.other_user = User.objects.create_user(username="other-service-user", password="StrongPass123!")
		self.category, _ = Category.objects.get_or_create(
			slug="hisob-kitob",
			defaults={"name": "Hisob-kitob"},
		)
		self.service, _ = Service.objects.get_or_create(
			slug="foiz-hisoblagich",
			defaults={
				"category": self.category,
				"name": "Foiz hisoblagich",
				"route": "/tools/percent",
			},
		)

	def test_catalog_endpoints_are_public(self):
		categories = self.client.get(reverse("category-list"))
		services = self.client.get(reverse("service-list"))

		self.assertEqual(categories.status_code, status.HTTP_200_OK)
		self.assertEqual(services.status_code, status.HTTP_200_OK)
		self.assertEqual(categories.data[0]["services"][0]["slug"], self.service.slug)

	def test_favorites_require_authentication_and_are_user_scoped(self):
		list_url = reverse("favorite-list-create")
		self.assertEqual(self.client.get(list_url).status_code, status.HTTP_401_UNAUTHORIZED)

		self.client.force_authenticate(self.user)
		response = self.client.post(list_url, {"service_slug": self.service.slug}, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Favorite.objects.filter(user=self.user).count(), 1)

		self.client.force_authenticate(self.other_user)
		response = self.client.get(list_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, [])

	def test_transactions_are_crud_scoped_to_authenticated_user(self):
		other_transaction = Transaction.objects.create(
			user=self.other_user,
			type="expense",
			amount="10.00",
			category="food",
			date=date(2026, 11, 6),
		)
		list_url = reverse("transaction-list-create")
		self.assertEqual(self.client.get(list_url).status_code, status.HTTP_401_UNAUTHORIZED)

		self.client.force_authenticate(self.user)
		response = self.client.post(
			list_url,
			{
				"type": "income",
				"amount": "123.45",
				"category": "salary",
				"description": "Audit income",
				"date": "2026-11-06",
			},
			format="json",
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		transaction_id = response.data["id"]
		self.assertEqual(Transaction.objects.get(pk=transaction_id).user, self.user)

		response = self.client.get(list_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual([item["id"] for item in response.data], [transaction_id])

		other_url = reverse("transaction-detail", kwargs={"pk": other_transaction.pk})
		self.assertEqual(self.client.get(other_url).status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(self.client.delete(other_url).status_code, status.HTTP_404_NOT_FOUND)
		self.assertTrue(Transaction.objects.filter(pk=other_transaction.pk).exists())

		own_url = reverse("transaction-detail", kwargs={"pk": transaction_id})
		response = self.client.patch(own_url, {"description": "Updated"}, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["description"], "Updated")

		response = self.client.delete(own_url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def test_legacy_finance_import_is_idempotent_and_never_overwrites(self):
		url = reverse("transaction-import-legacy")
		self.assertEqual(self.client.post(url, {"transactions": []}, format="json").status_code, status.HTTP_401_UNAUTHORIZED)
		self.client.force_authenticate(self.user)
		Transaction.objects.create(
			user=self.user, legacy_id="old-1", type="income", amount="7.00",
			category="salary", description="Keep existing", date=date(2026, 1, 1),
		)
		payload = {"transactions": [
			{"legacy_id": "old-1", "type": "expense", "amount": "99.00", "category": "food", "description": "Do not overwrite", "date": "2026-01-02"},
			{"legacy_id": "old-2", "type": "expense", "amount": "12.50", "category": "food", "description": "Imported", "date": "2026-01-03"},
		]}
		first = self.client.post(url, payload, format="json")
		second = self.client.post(url, payload, format="json")
		self.assertEqual(first.status_code, status.HTTP_200_OK)
		self.assertEqual(first.data["created"], 1)
		self.assertEqual(second.data["created"], 0)
		self.assertEqual(Transaction.objects.filter(user=self.user).count(), 2)
		self.assertEqual(Transaction.objects.get(user=self.user, legacy_id="old-1").description, "Keep existing")
		self.assertFalse(Transaction.objects.filter(user=self.other_user, legacy_id="old-2").exists())

	def test_transaction_list_can_filter_today_for_dashboard_totals(self):
		today = timezone.localdate()
		Transaction.objects.create(user=self.user, type="expense", amount="25.00", category="food", date=today)
		Transaction.objects.create(user=self.user, type="income", amount="100.00", category="salary", date=today)
		Transaction.objects.create(user=self.user, type="expense", amount="40.00", category="food", date=today - timedelta(days=1))
		self.client.force_authenticate(self.user)

		response = self.client.get(reverse("transaction-list-create"), {"date": today.isoformat()})

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual({item["type"] for item in response.data}, {"expense", "income"})
		self.assertEqual(sum(float(item["amount"]) for item in response.data if item["type"] == "expense"), 25.0)

	def test_transaction_amount_limit_applies_to_create_and_legacy_import(self):
		self.client.force_authenticate(self.user)
		create_url = reverse("transaction-list-create")
		payload = {
			"type": "expense", "amount": "1000000000000.01", "category": "food", "date": "2026-11-09",
		}
		response = self.client.post(create_url, payload, format="json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(str(response.data["amount"][0]), "Summa 1 trillion so‘mdan oshmasligi kerak.")
		self.assertFalse(Transaction.objects.filter(user=self.user).exists())

		payload["amount"] = "1000000000000.00"
		response = self.client.post(create_url, payload, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		import_url = reverse("transaction-import-legacy")
		response = self.client.post(import_url, {"transactions": [{
			"legacy_id": "too-large", "type": "expense", "amount": "1000000000000.01",
			"category": "food", "date": "2026-11-09",
		}]}, format="json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(str(response.data["transactions"][0]["amount"][0]), "Summa 1 trillion so‘mdan oshmasligi kerak.")
