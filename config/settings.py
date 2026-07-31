"""
Django settings for config project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*a^)t8oct&2a3el9ahk856$p^ew35zd1i+iw-1i*n#&-kw-_ja'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    'unfold',  # Должен быть ДО django.contrib.admin
    'unfold.contrib.filters',  # Кастомные фильтры Unfold
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Дополнительные приложения
    'rest_framework',
    'corsheaders',
    'products',  # Наше приложение для товаров
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Должен быть в самом верху
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'ru-ru'  # ← Меняем на русский
TIME_ZONE = 'Asia/Bishkek'  # ← Меняем на Бишкек
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (загруженные пользователем файлы)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ========== DRF (Django REST Framework) ==========
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Для разработки
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# ========== CORS ==========
# Разрешаем все источники для разработки
CORS_ALLOW_ALL_ORIGINS = True
ALLOWED_HOSTS = ['*']
# Для продакшена раскомментируй:
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:5173",
#     "https://telephone-osh.vercel.app",
#     "https://telephone-osh.onrender.com",
# ]

# ========== UNFOLD ADMIN THEME CONFIGURATION ==========
from django.urls import reverse_lazy
# config/settings.py (уже есть, проверь что все правильно)

UNFOLD = {
    "SITE_TITLE": "Телефон Ош",
    "SITE_HEADER": "Телефон Ош — Администрирование",
    "SITE_SUBTITLE": "Современная панель управления каталогом",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": False,
    "THEME": "dark",  # dark / light
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Управление товарами",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Все товары",
                        "icon": "shopping_bag",
                        "link": lambda request: reverse_lazy("admin:products_product_changelist"),
                    },
                    {
                        "title": "Фотографии товаров",
                        "icon": "photo_library",
                        "link": lambda request: reverse_lazy("admin:products_productimage_changelist"),
                    },
                ],
            },
            {
                "title": "Пользователи и Доступ",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": "Пользователи",
                        "icon": "person",
                        "link": lambda request: reverse_lazy("admin:auth_user_changelist"),
                    },
                    {
                        "title": "Группы",
                        "icon": "group",
                        "link": lambda request: reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },
}