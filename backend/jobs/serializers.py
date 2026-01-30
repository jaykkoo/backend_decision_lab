from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class JobCreateSerializer(serializers.Serializer):
    payload = serializers.DictField()


class JobCompleteSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["DONE", "FAILED"])
    result = serializers.JSONField(required=False)
    error = serializers.CharField(required=False)
    average_age = serializers.FloatField(required=False)
