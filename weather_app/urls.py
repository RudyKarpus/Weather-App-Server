from django.urls import path

from . import views

urlpatterns = [
    path(
        "weekly/data/<str:latitude>/<str:longitude>/",
        views.WeeklyDataView.as_view(),
        name="weekly_data",
    ),
    path(
        "weekly/summary/<str:latitude>/<str:longitude>/",
        views.WeeklySummaryView.as_view(),
        name="weekly_summary",
    ),
]
