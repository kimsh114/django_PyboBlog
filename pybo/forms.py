from django import forms

from pybo.models import Question, Answer, Comment

# 이러한 클래스를 장고의 폼이라고 한다.

class QuestionForm(forms.ModelForm): # forms.form을 전달값으로 받으면 폼이라고 하고, forms.ModelForm을 상속 받으면 모델폼이라고 한다.
    # 모델폼은 이 모델과 연결된 폼이며, 모델폼의 객체를 저장하면 연결된 모델의 데이터를 저장할 수 있다.
    class Meta: # 장고의 모델 폼에는 반드시 메타 클래스를 가져야 하며, 메타 클래스에는 모델 폼이 사용할 모델과 모델의 필드들을 적어야 함.
        model = Question
        fields = ['subject', 'content']
        labels = {
            'subject': '제목',
            'content': '내용',
        }

# question_form.html의 {{ form.as_p }}에 부트스트랩 적용이 안되기 때문에 여기의 메타 클래스에 widgets 속성을 사용함.
#         widgets = {
#             'subject' : forms.TextInput(attrs = {'class': 'form-control'}),
#             'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
#         }
# 만약에 question_form.html에 {{ form.as_p }} 를 사용할 거면 이 widgets 항목을 추가해줘야 조금이라도 css가 가능해짐

        # labels 속성을 이용해 subject와 content를 한글로 변경함.


# 답변 등록 기능에 장고 폼 적용하기
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글 내용',
        }