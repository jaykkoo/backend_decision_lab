from django.contrib import admin
from .models import Job, JobRun

# Register your models here.
admin.site.register(Job)
admin.site.register(JobRun)