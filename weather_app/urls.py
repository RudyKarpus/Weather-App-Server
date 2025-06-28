from django.urls import path

from . import views

urlpatterns = [
    path(
        "weekly/data/<str:latitude>/<str:longitude>/",
        views.WeeklyDataView.as_view(),
        name="weekly data",
    ),
    path(
        "weekly/summary/<str:latitude>/<str:longitude>/",
        views.WeeklySummaryView.as_view(),
        name="weekly summary",
    ),
]
