from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Conversation, Message
from .services import AIUnavailableError
from .throttles import AIRequestDailyThrottle, AIRequestMinuteThrottle

User = get_user_model()


class AIAPITests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="ai-user", password="StrongPass123!")
		self.other_user = User.objects.create_user(username="other-ai-user", password="StrongPass123!")

	def test_purposes_are_public(self):
		response = self.client.get(reverse("ai-purposes"))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn({"value": "general", "label": "Umumiy AI"}, response.data)

	def test_conversations_require_authentication(self):
		response = self.client.get(reverse("ai-conversation-list"))
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_conversation_list_and_detail_are_user_scoped(self):
		own = Conversation.objects.create(user=self.user, title="My chat")
		other = Conversation.objects.create(user=self.other_user, title="Other chat")
		self.client.force_authenticate(self.user)

		response = self.client.get(reverse("ai-conversation-list"))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual([item["id"] for item in response.data], [own.id])

		other_url = reverse("ai-conversation-detail", kwargs={"pk": other.pk})
		self.assertEqual(self.client.get(other_url).status_code, status.HTTP_404_NOT_FOUND)
		self.assertEqual(self.client.delete(other_url).status_code, status.HTTP_404_NOT_FOUND)
		self.assertTrue(Conversation.objects.filter(pk=other.pk).exists())

	@patch("apps.ai.views.generate_reply", return_value="Sinov javobi")
	@patch("apps.ai.views.is_configured", return_value=True)
	def test_message_uses_mocked_provider_and_persists_both_messages(self, _configured, generate):
		conversation = Conversation.objects.create(user=self.user, purpose="general")
		self.client.force_authenticate(self.user)

		response = self.client.post(
			reverse("ai-send-message", kwargs={"pk": conversation.pk}),
			{"content": "Salom"},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(response.data["ai_ok"])
		self.assertEqual(response.data["assistant_message"]["content"], "Sinov javobi")
		self.assertEqual(Message.objects.filter(conversation=conversation).count(), 2)
		generate.assert_called_once()

	@patch("apps.ai.views.generate_reply")
	@patch("apps.ai.views.is_configured", return_value=False)
	def test_missing_api_key_returns_clear_unconfigured_message(self, _configured, generate):
		conversation = Conversation.objects.create(user=self.user, purpose="general")
		self.client.force_authenticate(self.user)

		response = self.client.post(
			reverse("ai-send-message", kwargs={"pk": conversation.pk}),
			{"content": "Salom"},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertFalse(response.data["ai_configured"])
		self.assertFalse(response.data["ai_ok"])
		self.assertIn("AI_API_KEY", response.data["assistant_message"]["content"])
		generate.assert_not_called()

	@patch(
		"apps.ai.views.generate_reply",
		side_effect=AIUnavailableError("provider failure"),
	)
	@patch("apps.ai.views.is_configured", return_value=True)
	def test_provider_failure_does_not_break_message_endpoint(self, _configured, _generate):
		conversation = Conversation.objects.create(user=self.user, purpose="general")
		self.client.force_authenticate(self.user)

		response = self.client.post(
			reverse("ai-send-message", kwargs={"pk": conversation.pk}),
			{"content": "Salom"},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertFalse(response.data["ai_ok"])
		self.assertIn("AI xizmati vaqtincha", response.data["assistant_message"]["content"])

	def test_ai_message_endpoint_has_per_user_minute_and_daily_limits(self):
		conversation = Conversation.objects.create(user=self.user, purpose="general")
		self.client.force_authenticate(self.user)
		url = reverse("ai-send-message", kwargs={"pk": conversation.pk})

		minute_rates = {**AIRequestMinuteThrottle.THROTTLE_RATES, "ai_per_minute": "1/min"}
		daily_rates = {**AIRequestDailyThrottle.THROTTLE_RATES, "ai_per_day": "5/day"}
		with patch.object(AIRequestMinuteThrottle, "THROTTLE_RATES", minute_rates), patch.object(AIRequestDailyThrottle, "THROTTLE_RATES", daily_rates), patch("apps.ai.views.is_configured", return_value=False):
			cache.clear()
			first = self.client.post(url, {"content": "Birinchi xabar"}, format="json")
			second = self.client.post(url, {"content": "Ikkinchi xabar"}, format="json")

		self.assertEqual(first.status_code, status.HTTP_201_CREATED)
		self.assertEqual(second.status_code, status.HTTP_429_TOO_MANY_REQUESTS)
		self.assertIn("So'rovlar limiti tugadi", second.data["detail"])

		daily_rates = {**AIRequestDailyThrottle.THROTTLE_RATES, "ai_per_day": "1/day"}
		minute_rates = {**AIRequestMinuteThrottle.THROTTLE_RATES, "ai_per_minute": "10/min"}
		with patch.object(AIRequestMinuteThrottle, "THROTTLE_RATES", minute_rates), patch.object(AIRequestDailyThrottle, "THROTTLE_RATES", daily_rates), patch("apps.ai.views.is_configured", return_value=False):
			cache.clear()
			self.assertEqual(self.client.post(url, {"content": "Kunlik limit bir"}, format="json").status_code, status.HTTP_201_CREATED)
			self.assertEqual(self.client.post(url, {"content": "Kunlik limit ikki"}, format="json").status_code, status.HTTP_429_TOO_MANY_REQUESTS)

	def test_ai_message_validation_is_localized(self):
		self.client.force_authenticate(self.user)
		list_url = reverse("ai-conversation-list")
		res_uz = self.client.post(list_url, {"purpose": "invalid_purpose"}, format="json", HTTP_ACCEPT_LANGUAGE="uz")
		self.assertEqual(res_uz.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(res_uz.data["purpose"][0], "Noto'g'ri maqsad tanlandi.")

		res_ru = self.client.post(list_url, {"purpose": "invalid_purpose"}, format="json", HTTP_ACCEPT_LANGUAGE="ru")
		self.assertEqual(res_ru.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(res_ru.data["purpose"][0], "Выбрана неверная цель.")

		res_en = self.client.post(list_url, {"purpose": "invalid_purpose"}, format="json", HTTP_ACCEPT_LANGUAGE="en")
		self.assertEqual(res_en.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(res_en.data["purpose"][0], "Invalid purpose selected.")

