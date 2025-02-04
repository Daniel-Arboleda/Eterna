import os
from pathlib import Path
from decouple import config, Csv
from dotenv import load_dotenv
import environ
from datetime import timedelta
from django.core.cache import caches


# Define BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# Rutas de los archivos .env
general_env_path = BASE_DIR.parent / '.env'  # eterna_microservices/.env
microservice_env_path = BASE_DIR / '.env'   # auth_service/.env

# Depuración: Verificar si los archivos .env existen
print(f"Ruta general .env: {general_env_path}")
if not general_env_path.exists():
    print("El archivo general .env no existe en la ruta especificada.")

print(f"Ruta microservicio .env: {microservice_env_path}")
if not microservice_env_path.exists():
    print("El archivo del microservicio .env no existe en la ruta especificada.")

# Cargar las variables de entorno usando django-environ
env = environ.Env()

# Cargar el archivo .env general
environ.Env.read_env(str(general_env_path))

# Cargar el archivo .env del microservicio
environ.Env.read_env(str(microservice_env_path))

# Variables de entorno específicas de configuración
SECRET_KEY = env('SECRET_KEY', default='fallback-secret-key')
DEBUG = env('DEBUG', default='False', cast=bool)
ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='').split(',')

# Cargar variables de entorno para el entorno de desarrollo
load_dotenv()



# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',  # Aplicación interna de Django
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'roles',
    'user_sessions',  # Renombrado desde 'sessions'
    'password_reset',
    'two_factor_auth',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    # 'api',  # Cambia el nombre según corresponda
]

REST_FRAMEWORK = {  
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'SIGNING_KEY': os.getenv("JWT_SECRET_KEY", default='tu-clave-secreta-aqui'),
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_ISSUED_TOKENS': True,  # Habilita el blacklist de tokens
    'TOKEN_CACHE': caches['default'],  # Usa Redis para almacenar tokens
    'ALGORITHM': 'HS256',                         # Algoritmo de encriptación
    'SIGNING_KEY': os.getenv("JWT_SECRET_KEY", SECRET_KEY),                   # Clave de firma del token (usualmente tu SECRET_KEY)
    'AUTH_HEADER_TYPES': ('Bearer',),  # Asegúrate de usar este tipo de encabezado
}

# Configuración de Redis para Django
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # Cambia según tu configuración de Redis
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'auth_service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'auth_service.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME', default='default_db'),
        'USER': env('DB_USER', default='default_user'),
        'PASSWORD': env('DB_PASSWORD', default='default_password'),
        'HOST': env('DB_HOST', default='localhost'),
        'PORT': env('DB_PORT', default='5432'),
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]



# configurar un backend de correo de prueba en Django
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Para desarrollo



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}



# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de API Gateway y otros valores generales
API_GATEWAY_URL = env('API_GATEWAY_URL', default='http://localhost:8000')
COMMON_SECRET_KEY = env('COMMON_SECRET_KEY', default='fallback-common-secret-key')

AUTH_USER_MODEL = 'users.User'  # Asegúrate de que 'users.User' coincida con tu modelo de usuario personalizado

