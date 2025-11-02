import os
from celery import Celery

# تنظیم ماژول تنظیمات جنگو برای celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Customic.settings")

# ایجاد نمونه Celery
app = Celery("Customic")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
