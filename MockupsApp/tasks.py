from celery import shared_task
from django.conf import settings
from pathlib import Path

from .models import MockupRequest, MockupImage
from .services.renderer import render_text_on_shirt, ALL_SHIRT_COLORS

@shared_task(bind=True)
def generate_mockups_task(self, request_id: str):
    """
    تسک Celery: برای یک MockupRequest، به ازای هر رنگ یک تصویر می‌سازد،
    فایل‌ها را در media/mockups/ ذخیره می‌کند و رکوردهای MockupImage ایجاد می‌کند.
    """
    req = MockupRequest.objects.get(id=request_id)
    req.status = MockupRequest.Status.STARTED
    req.save(update_fields=["status"])

    try:
        colors = req.shirt_colors or list(ALL_SHIRT_COLORS)

        out_dir = Path(settings.MEDIA_ROOT) / "mockups"
        out_dir.mkdir(parents=True, exist_ok=True)

        for color in colors:
            img = render_text_on_shirt(
                text=req.text,
                shirt_color=color,
                font_name=req.font,
                text_color=req.text_color,
            )

            filename = f"{req.id}_{color}.jpg"
            out_path = out_dir / filename
            img.save(out_path, format="JPEG", quality=90)

            MockupImage.objects.create(
                request=req,
                shirt_color=color,
                image=f"mockups/{filename}",  # مسیر نسبی نسبت به MEDIA_ROOT
            )

        req.status = MockupRequest.Status.SUCCESS
        req.save(update_fields=["status"])
        return True

    except Exception as e:
        req.status = MockupRequest.Status.FAILURE
        req.save(update_fields=["status"])
        # برای لاگ بهتر می‌تونی از self.retry هم استفاده کنی، فعلاً استثنا را بالا می‌اندازیم
        raise e
