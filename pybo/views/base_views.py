
# 페이지를 추가하기 위한 import
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from ..models import Question
from django.db.models import Q,Count # OR 조건으로 데이터를 조회하는 장고의 함수이다.

def index(request):
    """
    pybo 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')  #localhost:8000/pybo/?page=1 과 같은 get 방식의 요청 url에서 page값을 가져올 때 사용됨
    #get('page','1') => /pybo/ 처럼 ?page=1과 같은 page 파라미터가 없는 URL을 위해 기본 값을 1로 지정함.
    kw = request.GET.get('kw', '') # 검색에 관한 것(kw = > keyword)
    so = request.GET.get('so', 'recent') # 정렬에 관한 것(so => sort)// 초기값 => 'recent' 최신순
    # 정렬
    #annotate(num_voter=Count('voter')) => Question 모델의 기존 필드에 질문의 추천수에 해당하는 num_voter을 임시로 추가해준다.
    # annotate 함수에서 이렇게 필드를 임시로 추가하면 filter 함수나 order_by 함수에서 num_voter 필드 사용이 가능하다.
    # num_voter 는 Count('voter')와 같이 Count 함수를 사용했다.

    if so == 'recommend': # 추천순(좋아요가 많은 순) // 추천수가 같으면 그 중 최신순으로 정렬
        question_list = Question.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular': # 인기순
        question_list = Question.objects.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # 최신순
        question_list = Question.objects.order_by('-create_date')

    # Question 모델 데이터를 작성한 날짜의 역순으로 조회하기 위해 order_by 함수를 사용함.
    if kw:
        question_list = question_list.filter( # 필터 함수에서 모델 필더에 접근하려면 __를 이용하면 됨.
            #icontains => 대소문자를 가리지 않고 찾아주는 기능이다.
            Q(subject__icontains = kw) | # 제목검색 // 제목에 kw 문자열이 포함되어있는지를 의미함.
            Q(content__icontains=kw) | # 내용검색
            Q(author__username__icontains=kw) | # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)# 답변 글쓴이 검색// 답변을 작성한 사람의 이름에 포함되는지를 의미함
        ).distinct()
        # distinct 함수는 조회 결과의 중복을 제거해 반환한다. (한개의 글에 여러 개의 답변이 있을 때 답변자 중복을 처리하기 위해 distinct함수를 반드시 사용해야함.)

    # 페이지 구현에 사용함// 한 페이지 당 10개씩 보여주자
    # Paginator 클래스는 question_list를 페이징 객체 paginator로 반환한다.
    paginator = Paginator(question_list, 7)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'page' : page, 'kw':kw, 'so' : so} # page와 kw가 추가됨.// 입력받은 page와 kw값을 템플릿의 SearchForm에 전달하기 위함.
    # 조회한 Question 모델 데이터는 context 변수에 저장함./ render 함수에서 템플릿을 HTML로 변환하는 과정에서 사용됨.

    return render(request, 'pybo/question_list.html', context)


def detail(request, question_id): # question_id => url 매핑에 있었던 것이 전달값으로 추가됨.
    """
    pybo 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id) # primary key인 question_id가 없으면 404 페이지를 반환하라.
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)





