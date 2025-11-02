from django.shortcuts import render

# Create your views here.

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from celery.result import AsyncResult
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import MockupRequest, MockupImage
from .serializers import MockupGenerateSerializer, MockupImageSerializer
from .tasks import generate_mockups_task


class GenerateMockupsAPIView(APIView):
    """
    POST /api/v1/mockups/generate/
    body: {text, font?, text_color?, shirt_color?=[white|black|blue|yellow]}
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = MockupGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        req = serializer.save()
        task = generate_mockups_task.delay(str(req.id))
        req.task_id = task.id
        req.save(update_fields=["task_id"])
        return Response(
            {"task_id": task.id, "status": "PENDING", "message": "Job queued"},
            status=status.HTTP_202_ACCEPTED
        )

class TaskStatusAPIView(APIView):
    """
    GET /api/v1/tasks/<task_id>/
    """
    permission_classes = [AllowAny]
    
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        payload = {"task_id": task_id, "status": result.status}

        if result.status == "SUCCESS":
            req = get_object_or_404(MockupRequest, task_id=task_id)
            images = MockupImage.objects.filter(request=req).order_by("-created_at")
            payload["results"] = MockupImageSerializer(
                images, many=True, context={"request": request}
            ).data

        return Response(payload, status=200)

class MockupHistoryListAPIView(generics.ListAPIView):
    """
    GET /api/mockups/?q=<text>&color=<white|black|blue|yellow>&page=&page_size=
    """
    serializer_class = MockupImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = MockupImage.objects.select_related("request").order_by("-created_at")
        q = self.request.query_params.get("q")
        color = self.request.query_params.get("color")

        if q:
            qs = qs.filter(request__text__icontains=q)
        if color:
            qs = qs.filter(shirt_color=color)

        return qs
