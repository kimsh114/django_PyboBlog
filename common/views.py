from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from .forms import UserForm


def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        # POST 요청인 경우 화면에서 입력한 데이터로 새로운 사용자를 생성
        form = UserForm(request.POST)
        # is_valid() =>  forms.py의 UserCreationForm의 함수로 회원가입 필드값 3개가 모두 입력되었는지, 모두 일치하는지 생성규칙이 모두 같은지 등을 검사하는 함수이다.
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # form.cleaned_data.get => 회원가입 화면에서 입력한 값을 얻기 위해 사용하는 함수.
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) # 회원가입이 된 이후 자동으로 로그인이 되도록 하기 위함.
            login(request, user)
            return redirect('index')
    else:
        # GET요청인 경우 common/signup.html 화면을 반환.
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})
