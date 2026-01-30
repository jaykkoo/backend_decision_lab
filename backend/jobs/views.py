from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from django.shortcuts import get_object_or_404
from .models import Job
from .serializers import (
    JobCreateSerializer, 
    JobSerializer,
    JobCompleteSerializer
)
from .services import enqueue_job, get_latency_by_volume


class ScoreBatchView(APIView):
    def post(self, request):
        serializer = JobCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        job = Job.objects.create(
            type="score_batch",
            payload=serializer.validated_data["payload"],
            status="PENDING",
        )

        enqueue_job(job)

        return Response(JobSerializer(job).data, status=201)


class JobDetailView(RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobCompleteView(APIView):
    def post(self, request, pk):
        print("🔥 JobCompleteView CALLED", pk, request.data)
        job = get_object_or_404(Job, pk=pk)
        serializer = JobCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.validated_data["result"]
        job.status = serializer.validated_data["status"]
        job.result = result
        job.save(update_fields=["status", "result"])

        JobRun.objects.create(
            job=job,
            engine=result["engine"],
            execution_time_ms=result["execution_time_ms"],
            processed_items=result["processed_items"],
        )

        return Response({"ok": True})

class JobStatsView(APIView):
    def get(self, request):
        return Response(get_latency_by_volume())