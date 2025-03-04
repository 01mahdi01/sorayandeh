import os
from tempfile import template

from config.env import env, BASE_DIR
from datetime import timedelta

env.read_env(os.path.join(BASE_DIR, ".env"))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "=ug_ucl@yi6^mrcjyz%(u0%&g2adt#bz3@yos%#@*t#t!ypx=a"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])


# Application definition
LOCAL_APPS = [
    "sorayandeh.core.apps.CoreConfig",
    "sorayandeh.common.apps.CommonConfig",
    "sorayandeh.users.apps.UsersConfig",
    "sorayandeh.campaign.apps.CampaignConfig",
    "sorayandeh.finance.apps.FinanceConfig",
    "sorayandeh.applicant.apps.ApplicantConfig",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_filters",
    "django_celery_results",
    "django_celery_beat",
    "corsheaders",
    "drf_spectacular",
    "django_extensions",
    "django_elasticsearch_dsl",
    "azbankgateways",
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # http://whitenoise.evans.io/en/stable/django.html#using-whitenoise-in-development
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # 'django.middleware.csrf.CsrfViewMiddleware',
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # 'sorayandeh.applicant.middleware.AttachSchoolMiddleware',
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
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


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DB_HOST = env.str("DB_HOST", default="127.0.0.1")
DB_PORT = env.str("DB_PORT", default="5432")
DB_NAME = env.str("DB_NAME", default="sorayandeh")
DB_USER = env.str("DB_USER", default="sorayandeh")
DB_PASSWORD = env.str("DB_PASSWORD", default="123456789")

# Default database configuration using environment variables
DATABASES = {
    "default": env.db("DATABASE_URL", default=f"psql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"),
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# GitHub Workflow specific configuration
if os.environ.get("GITHUB_WORKFLOW"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
AUTH_USER_MODEL = "users.BaseUser"

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # Default for BaseUser
    "sorayandeh.applicant.backends.SchoolAuthenticationBackend",  # Custom backend for School
]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "sorayandeh.api.exception_handlers.drf_default_with_modifications_exception_handler",
    # 'EXCEPTION_HANDLER': 'sorayandeh.api.exception_handlers.hacksoft_proposed_exception_handler',
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework_simplejwt.authentication.JWTAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),  # Adjust this to your desired expiration time
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),  # Adjust this as well if needed
    # Other configurations you might need:
    "ROTATE_REFRESH_TOKENS": True,  # Automatically issues a new refresh token with every refresh request
    "BLACKLIST_AFTER_ROTATION": True,  # Blacklists old refresh tokens upon rotation
}

# Redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_LOCATION", default="redis://localhost:6379"),
    }
}
# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 15


APP_DOMAIN = env("APP_DOMAIN", default="http://localhost:8000")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# CSRF_TRUSTED_ORIGINS = [
#     "https://sorayandeh-mahdi01.kubarcloud.net"
# ]
# CORS_ALLOW_ALL_ORIGINS = True
#
# CORS_ALLOWED_ORIGINS = [
#     "https://sorayandeh-mahdi01.kubarcloud.net",
# ]


CSRF_TRUSTED_ORIGINS = [
    "https://sorayandeh-mahdi01.kubarcloud.net",
    "http://sorayandeh-mahdi01.kubarcloud.net",
]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "https://sorayandeh-mahdi01.kubarcloud.net",
    "http://sorayandeh-mahdi01.kubarcloud.net",
]
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.yourdomain\.com$",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

ELASTICSEARCH_DSL = {
    "default": {"hosts": "http://elasticsearch:9200"},  # Change if running remotely
}
ELASTICSEARCH_DSL_AUTOSYNC = True


AZ_IRANIAN_BANK_GATEWAYS = {
    "GATEWAYS": {
        "ZARINPAL": {
            "MERCHANT_CODE": "412ee5c5-2da0-4932-bd61-9a6e93727294",
            "SANDBOX": 1,  # 0 disable, 1 active
        },
    },
    "IS_SAMPLE_FORM_ENABLE": True,  # اختیاری و پیش فرض غیر فعال است
    "DEFAULT": "ZARINPAL",
    "CURRENCY": "IRR",  # اختیاری
    "TRACKING_CODE_QUERY_PARAM": "tc",  # اختیاری
    "TRACKING_CODE_LENGTH": 16,  # اختیاری
    "SETTING_VALUE_READER_CLASS": "azbankgateways.readers.DefaultReader",  # اختیاری
      # اختیاری
    "IS_SAFE_GET_GATEWAY_PAYMENT": False,  # اختیاری، بهتر است True بزارید.
    "CUSTOM_APP": None,  # اختیاری
    'CALLBACK_NAMESPACE': 'finance:callback_gateway',
}
# Redirect all HTTP requests to HTTPS
# SECURE_SSL_REDIRECT = True
#
# # Ensure cookies (e.g., session, CSRF) are only sent over HTTPS
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
#
# # Optional: Set HSTS to tell browsers to always use HTTPS
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True


from config.settings.cors import *  # noqa
from config.settings.jwt import *  # noqa
from config.settings.sessions import *  # noqa
# from config.settings.celery import *  # noqa
from config.settings.swagger import *  # noqa

# from config.settings.sentry import *  # noqa
# from config.settings.email_sending import *  # noqa
