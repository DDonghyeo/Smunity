"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-@2^=jof@+(3es+wo!s$i!)t-a4_1**ql4co0*+y-xy*tlm8m6+')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get('DEBUG', 1))

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost 127.0.0.1').split(' ')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'graduations',
    'core',
]

MIDDLEWARE = [
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
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': os.environ.get("SQL_ENGINE", 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('SQL_DATABASE', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.environ.get('SQL_USER', 'user'),
        'PASSWORD': os.environ.get('SQL_PASSWORD', 'password'),
        'HOST': os.environ.get('SQL_HOST', 'localhost'),
        'PORT': os.environ.get("SQL_PORT", '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://localhost:8000 http://127.0.0.1:8000').split(' ')

# 로그아웃시 이동하는 URL
LOGOUT_REDIRECT_URL = '/'

# 필드 도메인
COLLEGE_CHOICES = (("융합공과대학", "융합공과대학"), ("인문사회과학대학", "인문사회과학대학"), ("사범대학", "사범대학"), ("경영경제대학", "경영경제대학"), ("문화예술대학", "문화예술대학"))
YEAR_CHOICES = (("커스텀", "커스텀"), ("2017", "17학번"), ("2018", "18학번"), ("2019", "19학번"), ("2020", "20학번"), ("2021", "21학번"), ("2022", "22학번"), ("2023", "23학번"))
TYPE_CHOICES = (("1전선", "1전선"), ("1전심", "1전심"), ("교선", "교선"), ("교필", "교필"), ("1교직", "1교직"), ("1전필", "1전필"),  ("일선", "일선"))
SUBTYPE_CHOICES_E = (("전문지식탐구역량", "전문지식탐구역량"), ("창의적문제해결역량", "창의적문제해결역량"), ("융복합역량", "융복합역량"), ("다양성존중역량", "다양성존중역량"), ("윤리실천역량", "윤리실천역량"))
SUBTYPE_CHOICES_S = (("인문", "인문"), ("사회", "사회"), ("자연", "자연"), ("공학", "공학"), ("예술", "예술"))
CULTURES_1 = [{'number': 'HALR1032', 'name': '사고와표현', 'credit': 3, 'semester': '1, 2'}, {'number': 'HALR1050\nHALR1231', 'name': 'EnglishforAcademicPurpose\n기초수학', 'credit': 3, 'semester': '1, 2'}, {'number': 'HALR1238\nHALR1239', 'name': '컴퓨팅사고와데이터의이해\n알고리즘과게임콘텐츠', 'credit': 2, 'semester': '1 | 2'}]
CULTURES_2 = [{'number': 'HALR1032', 'name': '사고와표현', 'credit': 3, 'semester': '1, 2'}, {'number': 'HALR1050\nHALR1231', 'name': 'EnglishforAcademicPurpose\n기초수학', 'credit': 3, 'semester': '1, 2'}, {'number': 'HALR1238', 'name': '컴퓨팅사고와데이터의이해', 'credit': 2, 'semester': '1'}, {'number': 'HALR1239', 'name': '알고리즘과게임콘텐츠', 'credit': 2, 'semester': '2'}]
CULTURES_DIC1 = [['사고와표현'], ['English', '영어', '수학', '미적분학'], ['컴퓨팅사고', '알고리즘']]
CULTURES_DIC2 = [['사고와표현'], ['English', '영어', '수학', '미적분학'], ['컴퓨팅사고'], ['알고리즘']]
