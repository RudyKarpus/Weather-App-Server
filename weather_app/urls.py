from django.urls import path

from . import views

urlpatterns = [
    path("weekly/data", views.WeeklyDataView.as_view(), name="weekly data"),
    path("weekly/summary", views.WeeklySummaryView.as_view(), name="weekly summary"),
]
