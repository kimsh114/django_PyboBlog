from django.urls import path
from .views import base_views, question_views, answer_views, comment_views, vote_views
# 파이보앱 이외에 다른 앱에서 같은 별칭 사용은 불가능 하다. => 이를 해결하기 위해 네임스페이스라는 독립된 이름 공간이 필요하다.

app_name = 'pybo'  # 이게 네임스페이스이다. // 네임스페이스를 설정해줬으면 템플릿에서도 바꿔야 한다.

urlpatterns = [
# config/urls.py 파일에서 pybo/에 대한 처리를 한 상태에서 pybo/urls.py 파일이 실행되므로 첫 번쨰 매개변수에 빈 문자열을 인자로 넘겨준다.

# base_views.py

    path('', base_views.index, name='index'),
    path('<int:question_id>/', base_views.detail, name='detail'),


# question_views.py

# 'name = ' 이것은 url에 별칭을 부여하는 것이다. 별칭을 부여해 url을 더 용이하게 관리할 수 있다.
    # pybo/2/가 요청이 되면 이 매핑 규칙에 의해 pybo/<int:question_id>가 적용되어 저장된다.// url에 공백이 있으면 안됨.
    # pybo/2/ 페이지가 호출이 되면 최종적으로 detail 함수의 전달값인 question_id에 2가 전달이 됨.
    path('question/create/', question_views.question_create, name='question_create'),
    path('question/modify/<int:question_id>/', question_views.question_modify, name = 'question_modify'),
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),

# answer_views.py

    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name = 'answer_modify'),
    path('question/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),


# comment_views.py

# 질문 댓글 등록// 댓글을 등록할 때는 question_id가 필요
    path('comment/create/question/<int:question_id>', comment_views.comment_create_question, name = 'comment_create_question'),
    path('comment/modify/question/<int:comment_id>', comment_views.comment_modify_question, name='comment_modify_question'),
    path('comment/delete/question/<int:comment_id>', comment_views.comment_delete_question, name='comment_delete_question'),# 질문 댓글 삭제// comment_id를 삭제함.
   # 답변 댓글 등록
    path('comment/create/answer/<int:answer_id>', comment_views.comment_create_answer, name='comment_create_answer'),
    path('comment/modify/answer/<int:comment_id>', comment_views.comment_modify_answer, name='comment_modify_answer'),
    path('comment/delete/answer/<int:comment_id>', comment_views.comment_delete_answer, name='comment_delete_answer'),

# vote_views.py

    path('vote/question/<int:question_id>/', vote_views.vote_question, name = 'vote_question'),
    path('vote/answer/<int:answer_id>/', vote_views.vote_answer, name = 'vote_answer'),
]
