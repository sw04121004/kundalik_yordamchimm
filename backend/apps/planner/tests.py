from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task

User = get_user_model()


class PlannerAPITests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="planner-user", password="StrongPass123!")
		self.other_user = User.objects.create_user(username="other-user", password="StrongPass123!")
		self.list_url = reverse("task-list-create")
		self.client.force_authenticate(self.user)

	def test_task_crud_and_user_assignment(self):
		response = self.client.post(
			self.list_url,
			{"title": "Audit task", "due_date": "2026-11-06", "due_time": "10:30"},
			format="json",
		)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		task_id = response.data["id"]
		task = Task.objects.get(pk=task_id)
		self.assertEqual(task.user, self.user)

		response = self.client.get(self.list_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual([item["id"] for item in response.data], [task_id])

		detail_url = reverse("task-detail", kwargs={"pk": task_id})
		response = self.client.patch(detail_url, {"is_done": True}, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertTrue(response.data["is_done"])

		response = self.client.delete(detail_url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		self.assertFalse(Task.objects.filter(pk=task_id).exists())

	def test_user_cannot_read_update_or_delete_another_users_task(self):
		task = Task.objects.create(user=self.other_user, title="Private task")
		detail_url = reverse("task-detail", kwargs={"pk": task.pk})

		self.assertEqual(self.client.get(detail_url).status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(
			self.client.patch(detail_url, {"is_done": True}, format="json").status_code,
			status.HTTP_404_NOT_FOUND,
		)
		self.assertEqual(self.client.delete(detail_url).status_code, status.HTTP_404_NOT_FOUND)
		task.refresh_from_db()
		self.assertFalse(task.is_done)

	def test_blank_title_is_rejected(self):
		response = self.client.post(self.list_url, {"title": "   "}, format="json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_date_filter_returns_only_matching_tasks(self):
		Task.objects.create(user=self.user, title="Today", due_date="2026-11-06")
		Task.objects.create(user=self.user, title="Tomorrow", due_date="2026-11-07")

		response = self.client.get(self.list_url, {"date": "2026-11-06"})
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual([item["title"] for item in response.data], ["Today"])
