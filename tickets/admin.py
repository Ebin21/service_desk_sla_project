from django.contrib import admin
from .models import Ticket, TicketComment

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "priority", "status", "requester", "assigned_to", "created_at", "due_at")
    list_filter = ("status", "priority", "category")
    search_fields = ("title", "description", "requester__username", "assigned_to__username")
    readonly_fields = ("created_at", "updated_at", "resolved_at")

@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ("ticket", "author", "created_at")
    search_fields = ("body",)
