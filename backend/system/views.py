from rest_framework.views import APIView
from rest_framework.response import Response
import httpx
import os

class HealthCheckView(APIView):
    def get(self, request):
        rust_status = "unreachable"
        try:
            with httpx.Client(timeout=1.0) as client:
                client.get(os.getenv("RUST_ENGINE_URL") + "/health")
            rust_status = "reachable"
        except Exception:
            pass

        return Response({
            "django": "ok",
            "rust_engine": rust_status,
        })
