from django.contrib.auth.models import User #User => django.contrib.auth에서 제공하는 모델이다.

from django.db import models # 장고는 이 모델을 이용해서 db의 실체가 될 테이블을 만든다.



class Question(models.Model):  # 이건 질문 모델이다.

    modify_date = models.DateTimeField(null=True, blank=True) # 질문 수정일자를 구현하기 위함.
# null=True => 데이터 베이스에서 modify_date 칼럼에  null을 허용한다.//  blank=True=> form.is_valid()를 통한 입력 폼 데이터 검사 시 값이 없어도 됨.
    #null=True/ blank=True => 한 마디로 어떤 조건이든 값을 비워둘 수 있다라는 의미이다.

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'author_question') # 모델에 글쓴이가 누구인지 추가하는 과정
    # User => 아래의 voter 필드와 같이 User 모델을 동시에 참고하고 있는 경우 migrations 시에 에러가 뜸. 오류 힌트의 related_name 옵션을 추가해야 함.
    #related_name = 'author_question' => 이런 식으로 하면 특정 사용자가 작성한 질문을 얻기 위해 some_user.author_question.all()과 같은 코드사용이 가능

    subject = models.CharField(max_length=200) # 질문의 제목 // 글자수를 제한하고 싶은 데이터는 charField를 사용하자
    content = models.TextField() # 질문의 내용 // 글자수의 제한이 없는 데이터는 TextFiled를 사용한다.
    create_date = models.DateTimeField() # 질문 생성일자 // 날짜나 시간관련한 속성은 DateTimeField를 사용한다.
    voter = models.ManyToManyField(User , related_name = 'voter_question') # 좋아요(추천) 기능을 사용하기 위함
    # ManyToManyField는 장고에서 다대다(글 1개에 추천을 여러명이 볼 수 있고, 한 명이 여러 개의 글을 추천할 수 있음을 쉽게 알 수 있도록 하는 관계모델
    # User => 위의 author 필드와 같이 User 모델을 동시에 참고하고 있는 경우 migrations 시에 에러가 뜸. 오류 힌트의 related_name 옵션을 추가해야 함.



    def __str__(self): # 이 함수는 사람이 보기 편하도록 제목을 보여주는 함수이다.
        return self.subject


class Answer(models.Model): # 답변 모델이다.
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'author_answer')  # 모델에 글쓴이가 누구인지 추가하는 과정
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # ForeignKey = > 외래키// 다른 모델과의 연결을 의미한다.
    # on_delete = models.CASCADE => 답변에 연결된 질문이 삭제되면 답변도 함께 삭제되어라.
    content = models.TextField() # 답변내용
    create_date = models.DateTimeField() # 답변일자
    voter = models.ManyToManyField(User , related_name = 'voter_answer')

# 댓글 모델
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 댓글 글쓴이
    content = models.TextField() # 댓글의 내용
    create_date = models.DateTimeField() # 댓글 생성일자
    modify_date = models.DateTimeField(null=True, blank=True) # 댓글 수정일시
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE) # 질문에 댓글 작성시 question  필드의 값에 저장이 됨.
    answer = models.ForeignKey(Answer, null=True, blank=True,on_delete=models.CASCADE) # 답변에 댓글이 작성되면 answer에 필드값이 저장됨.
# Comment 모델 데이터에는 question 필드 혹은 answer 필드 둘 중 하나에만 값이 저장이 되므로 null=True, blank=True이어야 함.
# 모델이 변경이 되면 항상 터미널에 python manage.py migrations => python manage.py migrate를 하자 ( 데이터베이스가 변경이 되었으므로)


