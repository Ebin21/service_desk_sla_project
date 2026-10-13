from django.urls import path
from . import views

urlpatterns = [
    path("", views.ticket_list, name="ticket_list"),
    path("new/", views.ticket_create, name="ticket_create"),
    path("<int:pk>/", views.ticket_detail, name="ticket_detail"),
    path("<int:pk>/edit/", views.ticket_update, name="ticket_update"),
    path("<int:pk>/delete/", views.ticket_delete, name="ticket_delete"),
    path("reports/export.csv", views.export_csv, name="export_csv"),
]
