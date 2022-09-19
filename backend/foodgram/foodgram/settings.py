import os

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, "../../infra/.env")
load_dotenv(dotenv_path)
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = False
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.CustomUser"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")
CORS_URLS_REGEX = r"^/api/.*$"
ROOT_URLCONF = "foodgram.urls"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

ALLOWED_HOSTS = [
    "localhost",
    "foodgram.freedynamicdns.org",
    "127.0.0.1",
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "corsheaders",
    "recipes.apps.RecipesConfig",
    "api.apps.ApiConfig",
    "users.apps.UsersConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:5000",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "../../docs")],
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

WSGI_APPLICATION = "foodgram.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

DEFAULT_PAGINATION_CLASS = "rest_framework.pagination.LimitOffsetPagination"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
    ),
    "UPLOADED_FILES_USE_URL": True,
    "DEFAULT_PAGINATION_CLASS": DEFAULT_PAGINATION_CLASS,
    "PAGE_SIZE": 999,
}

DJOSER = {
    "SERIALIZERS": {
        "user_create": "users.serializers.CustomUserSerializer",
        "user": "users.serializers.CustomUserSerializer",
        "user_delete": "djoser.serializers.UserDeleteSerializer",
    },
    "PERMISSIONS": {"user_list": ["rest_framework.permissions.AllowAny"]},
    "SEND_CONFIRMATION_EMAIL": True,
    "HIDE_USERS": False,
}

PSWR_TEMP = "django.contrib.auth.password_validation."

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": PSWR_TEMP + "UserAttributeSimilarityValidator",
    },
    {
        "NAME": PSWR_TEMP + "MinimumLengthValidator",
    },
    {
        "NAME": PSWR_TEMP + "CommonPasswordValidator",
    },
    {
        "NAME": PSWR_TEMP + "NumericPasswordValidator",
    },
]
