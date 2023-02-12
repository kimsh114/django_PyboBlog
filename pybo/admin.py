from django.contrib import admin
from .models import Question
## 장고 admin을 사용하려면 슈퍼유저를 생성해야 한다. // 터미널에 python manage.py createsuperuser를 치자
## admin 생성 후 장고 개발서버에서 /admin을 하자.

class QuestionAdmin(admin.ModelAdmin): # 질문의 제목을 검색하여 찾게해주는 것을 만듦
    search_fields = ['subject'] # search_fields 를 이용해 검색기능을 만듦


admin.site.register(Question, QuestionAdmin) # 위의 검색기능도 register
# models에서 만든 Question 모델을 admin에 등록하는 과정이다.