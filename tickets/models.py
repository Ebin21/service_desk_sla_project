from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone

SLA_HOURS = {"CRITICAL": 4, "HIGH": 8, "MEDIUM": 24, "LOW": 72}

class Ticket(models.Model):
    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        CRITICAL = "CRITICAL", "Critical"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"
        CLOSED = "CLOSED", "Closed"

    title = models.CharField(max_length=160)
    description = models.TextField()
    category = models.CharField(max_length=80, default="General")
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.OPEN)
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="requested_tickets"
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="assigned_tickets"
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    due_at = models.DateTimeField(blank=True, null=True)
    resolved_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.due_at and self.created_at:
            self.due_at = self.created_at + timedelta(hours=SLA_HOURS[self.priority])
        if self.status in (self.Status.RESOLVED, self.Status.CLOSED) and not self.resolved_at:
            self.resolved_at = timezone.now()
        elif self.status in (self.Status.OPEN, self.Status.IN_PROGRESS):
            self.resolved_at = None
        super().save(*args, **kwargs)

    @property
    def is_sla_met(self):
        if not self.resolved_at or not self.due_at:
            return None
        return self.resolved_at <= self.due_at

    @property
    def sla_state(self):
        if self.status in (self.Status.RESOLVED, self.Status.CLOSED):
            return "Met" if self.is_sla_met else "Breached"
        return "Overdue" if self.due_at and timezone.now() > self.due_at else "Within SLA"

    def __str__(self):
        return f"SD-{self.pk or 'NEW'}: {self.title}"


class TicketComment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment on ticket {self.ticket_id}"
