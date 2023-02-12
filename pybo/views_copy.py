from django.contrib.auth.decorators import login_required
# 페이지를 추가하기 위한 import
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
# redirect => 함수에 전달된 값을 참고하여 페이지의 이동을 수행한다.
# context에 있는 Question 모델 데이터 question_list를 question_list.html 파일에 적용해 HTML 코드로 변환
# question_list.html 파일을 장고에서는 템플릿이라고 부른다. // 장고의 태그를 추가로 사용할 수 있는 HTML 파일이다.
# 탬플릿을 모아 저장할 디렉터리를 만들자 (mkdir templates)

from django.utils import timezone
from .forms import QuestionForm, AnswerForm, CommentForm
from django.contrib import messages
from .models import Question, Answer, Comment


def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  #localhost:8000/pybo/?page=1 과 같은 get 방식의 요청 url에서 page값을 가져올 때 사용됨
    #get('page','1') => /pybo/ 처럼 ?page=1과 같은 page 파라미터가 없는 URL을 위해 기본 값을 1로 지정함.

    # Question 모델 데이터를 작성한 날짜의 역순으로 조회하기 위해 order_by 함수를 사용함.
    question_list = Question.objects.order_by('-create_date') # order_by 함수는 조회한 데이터를 특성 속성으로 정렬함. create_date 앞에 -가 있으므로 역순임.

    # 페이지 구현에 사용함// 한 페이지 당 10개씩 보여주자
    # Paginator 클래스는 question_list를 페이징 객체 paginator로 반환한다.
    paginator = Paginator(question_list, 7)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    # 조회한 Question 모델 데이터는 context 변수에 저장함./ render 함수에서 템플릿을 HTML로 변환하는 과정에서 사용됨.

    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id): # question_id => url 매핑에 있었던 것이 전달값으로 추가됨.
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id) # primary key인 question_id가 없으면 404 페이지를 반환하라.
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

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
            return redirect('pybo:detail', question_id=question.id)
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


#답변수정함수
@login_required(login_url='common:login')
def answer_modify(request, answer_id):

    """
    pybo 답변수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer': answer, 'form': form}
    return render(request, 'pybo/answer_form.html', context)



#답변 삭제함수
@login_required(login_url='common:login')
def answer_delete(request, answer_id):

    answer = get_object_or_404(Question, pk=answer_id)
    if request.user != answer.author:  # 로그인한 사용자와 글쓴이가 동일한 경우에만 삭제할 수 있도록
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id = answer.question.id)


# 질문 댓글 생성 함수
@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # form에 임시저장(date 때문)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.question = question # 댓글은 질문에 달리는 것이므로 Comment 모델의 question 속성에 질문 객체를 저장함.
            comment.save() # date까지 다 넣었으니 저장
            return redirect('pybo:detail', question_id = question_id)

    else:
        form = CommentForm()

    context = {'form':form}
    return render (request, 'pybo/comment_form.html', context) # 댓글 저장 후에는 작성한 질문 상세 화면으로 리다이렉트 시킴

    # 질문 댓글 수정 함수
@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):

    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)

    if request.method == "POST": # POST 방식이면 입력된 값으로 댓글 업데이트.
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.question.id)
    else: # GET 방식이면 기존의 댓글을 조회해 폼에 반영
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

# 질문 댓글 삭제 함수
@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    comment = get_object_or_404(Comment, pk= comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글 삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id = comment.question.id)
    else:
        comment.delete()
    return  redirect('pybo:detail', question_id = comment.question.id)


# 답변 댓글 생성 함수
# 답변 댓글을 등록하거나 수정하기 위해 사용한 폼과 템플릿은 질문 댓글에서 사용한 CommentForm과 comment_form.html 파일을 재활용할 수 있다.
@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    """
    pybo 답글댓글등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
            # comment.answer.question=> 답변 댓글에서 question_id를 얻어내기 위해 answer를 통해 question을 참조함.
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

# 답변 댓글 수정 함수
@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    """
    pybo 답글댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)

# 답변 댓글 삭제 함수
@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    """
    pybo 답글댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)