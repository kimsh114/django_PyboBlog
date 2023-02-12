from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
# redirect => 함수에 전달된 값을 참고하여 페이지의 이동을 수행한다.
# context에 있는 Question 모델 데이터 question_list를 question_list.html 파일에 적용해 HTML 코드로 변환
# question_list.html 파일을 장고에서는 템플릿이라고 부른다. // 장고의 태그를 추가로 사용할 수 있는 HTML 파일이다.
# 탬플릿을 모아 저장할 디렉터리를 만들자 (mkdir templates)

from django.utils import timezone
from ..forms import  AnswerForm
from django.contrib import messages
from ..models import Question, Answer


# 로그인 애너테이션을 통해 로그인이 되었는지를 우선 검사한다.
# 로그아웃 상태에서 @login_required 애너테이션이 적용된 함수가 호출되면 자동으로 로그인 화면으로 이동할 것.
#login_url='common:login' => 이동해야할 로그인 url
@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    pybo 답변등록
    """
    # question_id url매핑의 정보값이 넘어온다.
    # request 이 매개변수에서는 question_detail.html에서 textarea에 입력된 데이터가 파이썬 객체에 담겨 넘어옴.
    # request 매개변수에서 넘어온 값을 추출하기 위한 코드가 request.POST.get('content') 이다.
    # request.POST.get('content') => POST 형식으로 전송된 form 데이터 항목 중 name이 content인 값을 의미함.
    # question.answer_set.create => models.py의 Question 모델을 통해 Answer 모델의 데이터를 생성하기 위함
    # question.answer_set => models.py에서 Answer 모델이 Question 모델을 외래키로 사용하고 있어서 이와 같은 표현을 사용가능.
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user  # 답변 글쓴이는 현재 로그인을 한 계정이므로 현재 로그인한 계정의 User 모델의 객체인 request.user를 사용
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format( resolve_url('pybo:detail', question_id=question.id), answer.id))
        #  resolve_url=> 실제 호출되는 URL을 문자열로 반환하는 장고 함수 이다.
# '{}#answer_{}'.format( resolve_url('pybo:detail', question_id=question.id), answer.id) => 앵커 기능을 활성화 하기 위해 .format과 resolve_url 함수를 사용
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)
 # 첫 번째 인수에는 이동할 페이지의 별칭을, 두 번째는 해당 URL에 전달해야하는 값을 입력
# redirect 전달받은 값을 명령한 페이지로 이동시킴


## 참고
## Question 모델이 아닌 Answer 모델을 통해 직접 데이터를 저장하는 코드
## question = get_object_or_404(Question, pk = question_id)
## answer = Answer(question = question, content = request.POST.get('content'), create_date = timezone.now())
## answer.save()



#답변수정함수
@login_required(login_url='common:login')
def answer_modify(request, answer_id):

    """
    pybo 답변수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id) # 오류 발생할 경우의 가정법이므로 이 redirect에는 스크롤초기화 문제를 잡기 위한 앵커 테그를 하지 않음.

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('{}#answer_{}'.format( resolve_url('pybo:detail', question_id= answer.question.id), answer.id))
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)



#답변삭제함수
@login_required(login_url='common:login')
def answer_delete(request, answer_id):

    answer = get_object_or_404(Question, pk=answer_id)
    if request.user != answer.author:  # 로그인한 사용자와 글쓴이가 동일한 경우에만 삭제할 수 있도록
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id = answer.question.id)
