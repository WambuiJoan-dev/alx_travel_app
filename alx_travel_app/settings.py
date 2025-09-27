import os
from pathlib import Path
import environ # 1. Import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Initialize environ and read the .env file
env = environ.Env(
    # Set casting default for SECRET_KEY to str
    DEBUG=(bool, False) 
)
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# 3. Use environment variables for sensitive data
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG') # Read DEBUG from .env, defaults to False

ALLOWED_HOSTS = []
# ... other standard settings ...

# 4. INSTALLED_APPS
INSTALLED_APPS = [
    # Django Defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party Apps
    'rest_framework',        # Django REST Framework
    'corsheaders',           # CORS Headers
    'drf_yasg',              # Swagger/OpenAPI

    # Local Apps
    'listings',              # The app you created
]

# ... middleware and other settings ...
# In settings.py

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # --- START REQUIRED ADMIN MIDDLEWARE ---
    'django.contrib.sessions.middleware.SessionMiddleware', # E410 (Order is important!)
    'django.contrib.auth.middleware.AuthenticationMiddleware', # E408
    'django.contrib.messages.middleware.MessageMiddleware', # E409
    # --- END REQUIRED ADMIN MIDDLEWARE ---
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # ... other middleware ...
]
# In settings.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates', # E403
        'DIRS': [], # You can add your main template directory here later
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 5. Database Configuration (MySQL)
DATABASES = {
    'default': env.db(
        'DATABASE_URL',
        default=f"mysql://{env('DB_USER')}:{env('DB_PASSWORD')}@{env('DB_HOST')}:{env('DB_PORT')}/{env('DB_NAME')}"
    )
}

# 6. CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Add your frontend URL here
]
CORS_ALLOW_CREDENTIALS = True 

# 7. DRF Settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}

# ... other standard settings (LANGUAGE_CODE, TIME_ZONE, etc.) ...

# Static files (CSS, JavaScript, Images)
# ...