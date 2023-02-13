"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent #.parent 를 하나 더 붙이는 이유는 기존의 settings.py는 mysite/config였는데
#이제는 mysite/config/settings까지 왔기 때문


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ls&1oied3t*np!^y6664m!j2-l%ie=8g$w-bjk_pjryzd#3y6b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # 이 디버그 항목은 개발자에게 여러 정보를 알려 주는 오류 화면이다. 실제 서비스에서는 False로 설정하자.

ALLOWED_HOSTS = ['15.165.87.71'] # 파이보 서비스를 배포하기 위해 내가 aws lightsail로 만든 나의 개인 주소를 여기 적어줌
# 고정 아이피를 추가하면 개발 서버로 접속할 시에 오류가 뜸. => 개발 환경과 서버 환경을 구분해줘야함.


# Application definition

INSTALLED_APPS = [ # 이 부분은 장고에 현재 설치된 앱들이다.
    # 내가 만든 모델의 테이블을 생성하려면 여기에 내가 만든 앱을 추가해야한다.
# 내가 만든 모델의 apps의 컨피그 클래스가 config/setting.py 파일의 INSTALLED_APPS 항목에 추가가 안되면 장고는 내가 만든 앱을 인식 못한다.
    'common.apps.CommonConfig', # common 파일에는 로그인과 로그아웃/ 회원가입을 구성하는 앱이 있다.
    'pybo.apps.PyboConfig', # 이렇게 내가 만든 앱을 추가한다.(앱을 만드려면 터미널에 django-admin startapp 앱이름 이렇게 치자)
    'django.contrib.admin',
    'django.contrib.auth',  # 이게 로그인과 로그아웃을 쉽게 구현할 수 있도록 하는 기본 앱이다.
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
# 내가 만든 모델을 추가를 했으면, 터미널에 python manage.py makemigrations를 한 이후 python manage.py migrate를 실행한다.
# makemigrations는 장고가 테이블 작업을 수행하기 위한 파일들을 생성하는 과정이다.
# pybo에 보면 migrations 안의 0001_initial에 내가 만든 모델이 생성된 것을 볼 수 있다.
# makemigrations 와 migrate 작업은 모델의 속성이 추가되거나 변경된 경우에만 실행하는 명령이므로, 단순히 매소드 하나가 바뀌었다고 해서 이 작업을 할 필요는 없다.
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
        'DIRS': [BASE_DIR / 'templates'], # 템플릿 디렉토리를 만든 이후 여기에 만든 디렉토리를 BASE_DIR로 적음. //여러 개도 등록이 가능하다.
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
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {  # 여기는 데이터베이스 설정하는 곳이다.
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ko-kr' # 언어를 설정하는 곳이다.

TIME_ZONE = 'Asia/Seoul' # 여기는 표준시간대를 설정하는 곳이다.

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    # C:/projects/mysite/static을 의미한다. (css나 js 등을 사용하려면 경로를 추가해야함.)
    # STATICFILES_DIRS에 static을 등록한 이후 mkdir static을 통해 mysite에 디렉토리를 만들자.
    # pybo 파일 밑에 static 파일을 만들어도 괜찮지만 관리의 용이성을 위해 mysite에 만듦.
]

# 로그인/로그아웃 성공후 이동하는 URL
LOGIN_REDIRECT_URL = '/' # 로그인 성공시에  지정한 URL로 이동하기 위함이다.
LOGOUT_REDIRECT_URL = '/'  # 로그아웃 성공시에 지정한 url로 이동하기 위함이다.
