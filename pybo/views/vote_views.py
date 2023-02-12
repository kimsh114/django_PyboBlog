from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
# redirect => 함수에 전달된 값을 참고하여 페이지의 이동을 수행한다.
# context에 있는 Question 모델 데이터 question_list를 question_list.html 파일에 적용해 HTML 코드로 변환
# question_list.html 파일을 장고에서는 템플릿이라고 부른다. // 장고의 태그를 추가로 사용할 수 있는 HTML 파일이다.
# 탬플릿을 모아 저장할 디렉터리를 만들자 (mkdir templates)

from django.contrib import messages
from ..models import Question,Answer


# 질문 추천 등록
@login_required(login_url='common:login')
def vote_question(request,question_id):
    question = get_object_or_404(Question ,pk = question_id)
    if request.user == question.author: # 자기 추천 방지 기능
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        question.voter.add(request.user)
        # Question 모델의 voter 필드는 ManyToManyField로 정의 했으므로 question.voter.add(request.user)와 같이 add함수로 추천인을 추가 해야 한다.
    return redirect('pybo:detail', question_id = question_id)

#답변 추천 등록
@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk = answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        answer.voter.add(request.user)
    return redirect('pybo:detail', question_id = answer.question.id)