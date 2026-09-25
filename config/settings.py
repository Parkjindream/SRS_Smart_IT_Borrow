"""
Django settings สำหรับระบบยืม-คืนอุปกรณ์ไอที (IT Equipment Borrowing System)
"""
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

# --- ความปลอดภัยพื้นฐาน (ดึงจาก .env เสมอ อย่า hardcode ในโค้ดจริง) ---
SECRET_KEY = config("DJANGO_SECRET_KEY", default="dev-only-secret-change-me")
DEBUG = config("DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "django_crontab",
    # โปรเจกต์ของเรา
    "rental",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --- Database: PostgreSQL ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="it_lending_db"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASSWORD", default="postgres"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default="5432"),
    }
}

# --- Custom User model (นักศึกษา / เจ้าหน้าที่) ---
AUTH_USER_MODEL = "rental.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "th"
TIME_ZONE = "Asia/Bangkok"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"  # เก็บ QR code / รูปอุปกรณ์

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Django REST Framework ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# --- CORS: ให้ frontend (HTML/Tailwind/JS ที่รันแยกพอร์ต) เรียก API ได้ ---
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:3000,http://127.0.0.1:5500",
    cast=Csv(),
)

# --- อีเมล (สำหรับระบบแจ้งเตือน โมดูล E) ---
EMAIL_BACKEND = config("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="no-reply@it-lending.local")

# --- Scheduled jobs (django-crontab) ---
# รันทุก 1 ชั่วโมง: เช็ค booking ที่ no-show (เลยเวลาหมดอายุการจอง)
# รันวันละครั้ง (เช่นตี 7): เช็คใกล้ครบกำหนด / ถึงกำหนด / เกินกำหนด
CRONJOBS = [
    ("0 * * * *", "rental.jobs.cancel_expired_bookings"),
    ("0 7 * * *", "rental.jobs.run_daily_due_date_checks"),
]

# --- ค่าตั้งต้นของระบบบทลงโทษ / เวลาหมดอายุการจอง ---
# ค่าจริงที่ปรับได้ผ่านแอดมินอยู่ในตาราง PenaltySettings (โมดูล F)
# ค่าพวกนี้ใช้เป็น fallback ตอน seed ข้อมูลครั้งแรกเท่านั้น
DEFAULT_BOOKING_EXPIRE_HOURS = 24
DEFAULT_MAX_BORROW_DAYS = 7
DEFAULT_OVERDUE_DAYS_THRESHOLD = 1
DEFAULT_SUSPENSION_DAYS = 2
