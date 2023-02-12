"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path # include는 url.py 파일을 pybo앱에 따로 구성을 하기 위해 사용함.

from pybo.views import base_views 
# 파이보 파일의 views파일의 base_views가 초기화면

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')),
    path('common/', include('common.urls')), # 로그인과 로그아웃을 구현하기 위해 common 파일을 include
    # include('pybo.urls') => pybo/로 시작되는 페이지 요청은 모두 pybo/urls.py 파일에 있는 url 매핑을 참고해서 처리하라는 의미이다.
    # 이 부분을 include 해준 순간부터 파이보앱의 url요청은 pybo/urls.py를 통해 처리가 된다.

    path('', base_views.index, name='index'),# /(슬래시) 페이지 요청에 대해 이 문장이 작동하여 pybo/views.py 파일의 index 함수가 실행이 된다.


]
