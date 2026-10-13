from datetime import timedelta
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Ticket

User = get_user_model()

class TicketModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="requester", password="Testpass123!")

    def test_ticket_gets_sla_due_date(self):
        ticket = Ticket.objects.create(
            title="Email access issue", description="Cannot access email",
            requester=self.user, priority=Ticket.Priority.HIGH
        )
        self.assertIsNotNone(ticket.due_at)
        self.assertEqual(ticket.due_at, ticket.created_at + timedelta(hours=8))

    def test_unresolved_ticket_is_not_sla_met(self):
        ticket = Ticket.objects.create(
            title="VPN issue", description="VPN fails", requester=self.user
        )
        self.assertIsNone(ticket.is_sla_met)

class TicketViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="agent", password="Testpass123!")

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_open_dashboard(self):
        self.client.login(username="agent", password="Testpass123!")
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
