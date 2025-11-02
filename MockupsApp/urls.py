from django.urls import path
from django.http import HttpResponse
from .views import GenerateMockupsAPIView, TaskStatusAPIView, MockupHistoryListAPIView

# Health check endpoint
def ping(request):
    return HttpResponse("ok")

urlpatterns = [
    path("ping", ping, name="ping"),
    path("v1/mockups/generate/", GenerateMockupsAPIView.as_view()),
    path("v1/tasks/<str:task_id>/", TaskStatusAPIView.as_view()),
    path("mockups/", MockupHistoryListAPIView.as_view())
]

