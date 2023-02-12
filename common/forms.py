from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):# django.contrib.auth.forms의 UserCreationForm클래스를 상속
    #UserCreationForm=> 사용자 이름과 비밀번호 입력 및 비밀번호 확인 기능까지 가지고 있다.
    email = forms.EmailField(label="이메일") #email 속성을 추가함.

    class Meta:
        model = User
        fields = ("username", "email")
