# پروژه‌ی Customic Mockup Generator

این پروژه به عنوان (**تسک فنی استخدامی شرکت Customic**) توسعه داده شده است.
هدف آن، پیاده‌سازی سیستمی برای **تولید خودکار موکاپ‌های تی‌شرت** با استفاده از Django REST Framework، Celery و Redis است.
در این پروژه، متن وارد شده توسط کاربر روی تصاویر تی‌شرت در رنگ‌های مختلف رندر می‌شود و فایل‌های خروجی به صورت خودکار در پوشه‌ی `media/` ذخیره می‌گردند.



#  تکنولوژی‌ها و ابزارهای استفاده‌شده

| ابزار / فریم‌ورک                  | توضیح                                    |
| --------------------------------- | ---------------------------------------- |
| **Python 3.13+**                  | زبان اصلی پروژه                          |
| **Django 5.x**                    | فریم‌ورک اصلی بک‌اند                     |
| **Django REST Framework (DRF)**   | ساخت APIها                               |
| **Celery 5.x**                    | اجرای غیربلاکینگ تسک‌ها                  |
| **Redis**                         | message broker برای Celery               |
| **Pillow**                        | رندر و ویرایش تصاویر تی‌شرت              |
| **drf-spectacular**               | مستندسازی خودکار APIها (Swagger / Redoc) |
| **djangorestframework-simplejwt** | احراز هویت با JWT                        |



## پیش‌نیازها

قبل از اجرای پروژه، مطمئن شوید موارد زیر نصب شده‌اند:

Python 3.13 یا بالاتر
Redis Server
(اختیاری) Git برای کلون کردن پروژه



#مراحل نصب و راه‌اندازی

# 1. کلون یا دریافت پروژه


git clone <repository-url>
cd Customic


# 2. ساخت و فعال‌سازی محیط مجازی (venv)


python -m venv .venv
source .venv/bin/activate   # در ویندوز: .venv\Scripts\activate


#3. نصب وابستگی‌ها


pip install -r requirements.txt


#4. اعمال مایگریشن‌ها و ایجاد پایگاه داده


python manage.py migrate


(اختیاری) ساخت حساب ادمین برای ورود به /admin:


python manage.py createsuperuser


#5. اجرای Redis Server

قبل از اجرای Celery باید Redis را راه‌اندازی کنید:


redis-server


در صورتی که Redis روی سیستم نصب نیست، از Docker هم می‌توانید استفاده کنید:


docker run -d -p 6379:6379 redis


#6. اجرای کارگر Celery

در یک ترمینال جداگانه:


celery -A Customic worker -l info


# 7. اجرای سرور Django

در ترمینال اصلی:


python manage.py runserver




# تست پروژه

# 1. ساخت موکاپ

ارسال درخواست POST به:


POST /api/v1/mockups/generate/


نمونه داده:

json
{
  "text": "Hello World",
  "font": "Vazirmatn.ttf",
  "text_color": "#000000",
  "shirt_color": ["white", "black"]
}


پاسخ اولیه:

json
{
  "task_id": "uuid-string",
  "status": "PENDING",
  "message": "Job queued"
}


# 2. بررسی وضعیت تسک


GET /api/v1/tasks/<task_id>/


خروجی در صورت موفقیت شامل لینک تصاویر ساخته‌شده است.

# 3. مشاهده تاریخچه (با احراز هویت JWT)


GET /api/mockups/?q=<text>&color=<color>


# نکات پایانی
پوشهٔ media/mockups/ محل ذخیرهٔ تصاویر نهایی است.
برای مشاهدهٔ داکیومنت Swagger:

 
http://127.0.0.1:8000/api/schema/swagger-ui/

 اطمینان حاصل کنید که Redis و Celery قبل از ارسال درخواست فعال باشند.
 در محیط Production مقدار `DEBUG` را روی `False` و کلید `SECRET_KEY` را به مقدار امن تغییر دهید.

