from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
# LoginView=> django.contrib.auth 앱의 LoginView 클래스를 활용했으므로 별도의 views.py의 수정이 필요 없다.
    # LoginView 클래스는 registration 이라는 템플릿에서 login.html 파일을 찾는다. // 게시판 기능만 별도로 로그인 기능을 구현하려면 외부에
    # registration 디렉토리를 만들어야 하지만 게시판 기능이 웹의 일부인 이 경우에는 그냥 common 디렉토리에 구성하자
    # template_name = 'common/login.html' => 이러면 외부의 registration 디렉토리에서 html을 찾는게 아닌 common 디렉토리에서 html을 찾는다.
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'), # 회원가입 링크를 누르면 common/views.py에서  signup 함수가 실행됨.
]