from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect, resolve_url
# redirect => 함수에 전달된 값을 참고하여 페이지의 이동을 수행한다.
# context에 있는 Question 모델 데이터 question_list를 question_list.html 파일에 적용해 HTML 코드로 변환
# question_list.html 파일을 장고에서는 템플릿이라고 부른다. // 장고의 태그를 추가로 사용할 수 있는 HTML 파일이다.
# 탬플릿을 모아 저장할 디렉터리를 만들자 (mkdir templates)

from django.utils import timezone
from ..forms import CommentForm
from django.contrib import messages
from ..models import Question, Answer, Comment



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
            return redirect('{}#comment_{}'.format( resolve_url('pybo:detail', question_id=comment.question.id), comment.id))

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
            return redirect('{}#comment_{}'.format( resolve_url('pybo:detail', question_id=comment.question.id), comment.id))

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
            return redirect('{}#comment_{}'.format( resolve_url('pybo:detail', question_id=comment.answer.question.id), comment.id))
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
            return redirect('{}#comment_{}'.format( resolve_url('pybo:detail', question_id=comment.answer.question.id), comment.id))
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