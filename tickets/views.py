import csv
from datetime import timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Count, Q, Avg, F, ExpressionWrapper, DurationField
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import TicketForm, TicketCommentForm
from .models import Ticket, TicketComment

@login_required
def dashboard(request):
    tickets = Ticket.objects.all()
    now = timezone.now()
    total = tickets.count()
    open_count = tickets.filter(status=Ticket.Status.OPEN).count()
    in_progress = tickets.filter(status=Ticket.Status.IN_PROGRESS).count()
    resolved = tickets.filter(status__in=[Ticket.Status.RESOLVED, Ticket.Status.CLOSED]).count()
    overdue = tickets.filter(
        due_at__lt=now
    ).exclude(status__in=[Ticket.Status.RESOLVED, Ticket.Status.CLOSED]).count()
    resolved_tickets = tickets.filter(
        status__in=[Ticket.Status.RESOLVED, Ticket.Status.CLOSED], resolved_at__isnull=False
    )
    resolved_with_sla = resolved_tickets.filter(resolved_at__lte=F("due_at")).count()
    resolved_total = resolved_tickets.count()
    sla_pct = round((resolved_with_sla / resolved_total) * 100, 1) if resolved_total else 0
    priority_data = list(tickets.values("priority").annotate(count=Count("id")).order_by("priority"))
    status_data = list(tickets.values("status").annotate(count=Count("id")).order_by("status"))
    category_data = list(tickets.values("category").annotate(count=Count("id")).order_by("-count")[:8])
    latest = tickets.select_related("requester", "assigned_to")[:8]
    context = {
        "total": total, "open_count": open_count, "in_progress": in_progress,
        "resolved": resolved, "overdue": overdue, "sla_pct": sla_pct,
        "priority_labels": [x["priority"].title() for x in priority_data],
        "priority_values": [x["count"] for x in priority_data],
        "status_labels": [x["status"].replace("_", " ").title() for x in status_data],
        "status_values": [x["count"] for x in status_data],
        "category_labels": [x["category"] for x in category_data],
        "category_values": [x["count"] for x in category_data],
        "latest": latest,
    }
    return render(request, "tickets/dashboard.html", context)

@login_required
def ticket_list(request):
    qs = Ticket.objects.select_related("requester", "assigned_to")
    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "")
    priority = request.GET.get("priority", "")
    category = request.GET.get("category", "").strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(category__icontains=q))
    if status:
        qs = qs.filter(status=status)
    if priority:
        qs = qs.filter(priority=priority)
    if category:
        qs = qs.filter(category__icontains=category)
    return render(request, "tickets/ticket_list.html", {
        "tickets": qs, "q": q, "selected_status": status,
        "selected_priority": priority, "category": category,
        "statuses": Ticket.Status.choices, "priorities": Ticket.Priority.choices,
    })

@login_required
def ticket_create(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.requester = request.user
            ticket.save()
            messages.success(request, f"Ticket SD-{ticket.pk} created.")
            return redirect("ticket_detail", pk=ticket.pk)
    else:
        form = TicketForm()
    return render(request, "tickets/ticket_form.html", {"form": form, "heading": "Create ticket"})

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket.objects.select_related("requester", "assigned_to"), pk=pk)
    if request.method == "POST":
        form = TicketCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            messages.success(request, "Update added.")
            return redirect("ticket_detail", pk=pk)
    else:
        form = TicketCommentForm()
    return render(request, "tickets/ticket_detail.html", {"ticket": ticket, "comment_form": form})

@login_required
def ticket_update(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, f"Ticket SD-{ticket.pk} updated.")
            return redirect("ticket_detail", pk=pk)
    else:
        form = TicketForm(instance=ticket)
    return render(request, "tickets/ticket_form.html", {"form": form, "heading": f"Edit SD-{ticket.pk}"})

@login_required
def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "POST":
        ticket_id = ticket.pk
        ticket.delete()
        messages.success(request, f"Ticket SD-{ticket_id} deleted.")
        return redirect("ticket_list")
    return render(request, "tickets/ticket_confirm_delete.html", {"ticket": ticket})

@login_required
def export_csv(request):
    qs = Ticket.objects.select_related("requester", "assigned_to")
    status = request.GET.get("status", "")
    priority = request.GET.get("priority", "")
    if status:
        qs = qs.filter(status=status)
    if priority:
        qs = qs.filter(priority=priority)
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="service_desk_tickets.csv"'
    writer = csv.writer(response)
    writer.writerow(["Ticket ID", "Title", "Category", "Priority", "Status", "Requester", "Assignee", "Created At", "Due At", "Resolved At", "SLA State"])
    for t in qs:
        writer.writerow([
            f"SD-{t.pk}", t.title, t.category, t.get_priority_display(), t.get_status_display(),
            t.requester.username, t.assigned_to.username if t.assigned_to else "",
            t.created_at.isoformat(), t.due_at.isoformat() if t.due_at else "",
            t.resolved_at.isoformat() if t.resolved_at else "", t.sla_state,
        ])
    return response
