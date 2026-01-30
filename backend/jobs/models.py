import uuid
from django.db import models

class Job(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("RUNNING", "Running"),
        ("DONE", "Done"),
        ("FAILED", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length=50)
    payload = models.JSONField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class JobRun(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="runs",
    )
    engine = models.CharField(max_length=20, null=True, blank=True)
    execution_time_ms = models.FloatField(null=True, blank=True)
    processed_items = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    average_age = models.FloatField(null=True, blank=True)

