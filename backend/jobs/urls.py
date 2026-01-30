from django.urls import path
from .views import (
    ScoreBatchView, 
    JobDetailView, 
    JobCompleteView, 
    JobStatsView,
)

urlpatterns = [
    path("score/batch/", ScoreBatchView.as_view(), name="score-batch"),
    path("<uuid:pk>/", JobDetailView.as_view(), name="job-detail"),
    path("<uuid:pk>/complete/", JobCompleteView.as_view(), name="job-complete"),
    path("stats/", JobStatsView.as_view(), name="job-stats"),
]
