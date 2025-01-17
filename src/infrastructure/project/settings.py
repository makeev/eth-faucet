"""
Django settings for main project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import logging
import os
from pathlib import Path

from eth_account import Account
from eth_account.signers.local import LocalAccount

logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS: list[str] = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "infrastructure",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "infrastructure.project.urls"

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

WSGI_APPLICATION = "infrastructure.project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "django_db"),
        "USER": os.getenv("POSTGRES_USER", "django_user"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "django_password"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": int(os.getenv("POSTGRES_PORT", 5432)),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "infrastructure.project.exception_handlers.custom_exception_handler",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": ("infrastructure.project.renderers.CustomJSONRenderer",),
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@localhost"

# App settings
BLOCKCHAIN_PROVIDER_URL = os.getenv("BLOCKCHAIN_PROVIDER_URL")
BLOCKCHAIN_CHAIN_ID = int(os.getenv("BLOCKCHAIN_CHAIN_ID", "0"))
if not BLOCKCHAIN_PROVIDER_URL or not BLOCKCHAIN_CHAIN_ID:
    raise ValueError("BLOCKCHAIN_PROVIDER_URL and BLOCKCHAIN_CHAIN_ID are required")

FAUCET_MNEMONIC_KEY = os.getenv("FAUCET_MNEMONIC_KEY")
FAUCET_PRIVATE_KEY = os.getenv("FAUCET_PRIVATE_KEY")


FAUCET_ACCOUNT: LocalAccount
if FAUCET_MNEMONIC_KEY:
    Account.enable_unaudited_hdwallet_features()
    FAUCET_ACCOUNT = Account.from_mnemonic(FAUCET_MNEMONIC_KEY)
    logger.info(f"Using account {FAUCET_ACCOUNT.address} from mnemonic phrase")
elif FAUCET_PRIVATE_KEY:
    FAUCET_ACCOUNT = Account.from_key(FAUCET_PRIVATE_KEY)
    logger.info(f"Using account {FAUCET_ACCOUNT.address} from private key")
else:
    raise ValueError("FAUCET_MNEMONIC_KEY or FAUCET_PRIVATE_KEY is required")

FAUCET_THRESHOLD_TIMEOUT_MINUTES = int(os.getenv("FAUCET_THRESHOLD_TIMEOUT_MINUTES", 1))
FAUCET_AMOUNT_ETH = os.getenv("FAUCET_AMOUNT_ETH", "0.0001")
