from django.db import models
# uuid برای فیلد شناسه یکتا
import uuid

# Create your models here.
# مدل درخواست موکاپ
class MockupRequest(models.Model):
    # وضعیت‌های ممکن برای پردازش موکاپ
    class Status(models.TextChoices):
        PENDING = "PENDING"
        STARTED = "STARTED"
        SUCCESS = "SUCCESS"
        FAILURE = "FAILURE"

	# فیلدهای مدل
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    font = models.CharField(max_length=64, blank=True, null=True)
    text_color = models.CharField(max_length=7, blank=True, null=True)  # Example:  "#000000"
    shirt_colors = models.JSONField(default=list)  # Example:  ["white","black","blue","yellow"]
    task_id = models.CharField(max_length=128, blank=True, null=True)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

	# نمایش رشته‌ای مدل
    def __str__(self):
        return f"{self.id} - {self.text[:20]}"

# مدل تصویر موکاپ
class MockupImage(models.Model):
    request = models.ForeignKey(MockupRequest, related_name="images", on_delete=models.CASCADE)
    shirt_color = models.CharField(max_length=16)
    image = models.ImageField(upload_to="mockups/")  # media/mockups/<file>
    created_at = models.DateTimeField(auto_now_add=True)

	# نمایش رشته‌ای مدل 
    def __str__(self):
        return f"{self.request_id} - {self.shirt_color}"

