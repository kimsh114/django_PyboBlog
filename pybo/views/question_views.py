from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
# redirect => 함수에 전달된 값을 참고하여 페이지의 이동을 수행한다.
# context에 있는 Question 모델 데이터 question_list를 question_list.html 파일에 적용해 HTML 코드로 변환
# question_list.html 파일을 장고에서는 템플릿이라고 부른다. // 장고의 태그를 추가로 사용할 수 있는 HTML 파일이다.
# 탬플릿을 모아 저장할 디렉터리를 만들자 (mkdir templates)

from django.utils import timezone
from ..forms import QuestionForm
from django.contrib import messages
from ..models import Question


@login_required(login_url='common:login')
# 질문생성 함수
def question_create(request):
    """
    pybo 질문등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST) # POST 방식의 경우 전달값을 주고, GET방식의 경우 전달값을 안 줘도 되도록 생성.
        if form.is_valid(): # POST 요청으로 받은 form이 유효한지를 검사한다.
            question = form.save(commit=False) # form 으로 Question 모델의 데이터를 저장하기 위한 코드
            #  commit=False => 임시저장을 의미함.// form으로 질문데이터를 저장하면 Question 모델의 create_date에 값이 설정되니 않아 오류가 발생함.
            question.author = request.user  # 추가한 속성 author 적용

            #request.user => 로그인 상태이면 User 객체가, 로그아웃 상태이면 AnnoymousUser 객체가 들어있다.
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm() # forms.py에서 QuestionForm 클래스를 사용 // 여기서 form은 장고의 폼이다.
        # request.method가 'GET'인 경우에 호출(전달값이 없도록 설계)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
# render 함수에서 context => 템플릿에서 폼 엘리먼트를 생성할 때 사용

@login_required(login_url='common:login')
def question_modify(request, question_id):
    '''pybo의 질문 수정함수'''
    question = get_object_or_404(Question, pk = question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.') # messages 모듈을 이용해 메시지 전달// 오류를 임의로 발생시키고 싶을 때 사용
        return  redirect('pybo:detail',question_id = question_id)
# question.detail의 수정하기 버튼을 누르면 Get방식으로 호출되어 질문 수정 화면이 나타나고, 질문 수정 화면에서 저장하기를 누르면 POST 방식으로 호출되어 데이터 수정이 이루어짐
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        #instance=question=> GET 요청으로 질문 수정 화면이 나타날 때 기존에 저장되어 있던 제목과 내용이 그대로 나타나게끔함.
        # instance 매개변수에 question을 지정하면 기존 값을 폼에 채울 수 있다.
#form = QuestionForm(request.POST, instance=question) 의 의미는 question 값을 기본으로 하며, 화면으로 전달받은 입력값들을 덮어써서 QuestionForm을 생성해라라는 의미이다.
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id = question_id)
    else:
        form = QuestionForm(instance=question)
    context = {'form' : form}
    return render(request, 'pybo/question_form.html',context) # 질문 수정에 사용할 테플릿은 question_form 파일을 그대로 사용한다.

# 질문 삭제 함수
@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    pybo 질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:  # 로그인한 사용자와 글쓴이가 동일한 경우에만 삭제할 수 있도록
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')