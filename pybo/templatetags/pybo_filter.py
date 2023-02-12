from django import template
#templatetags 파일은 무조건 앱 디렉토리 안에 만들어야 한다.
import markdown
from django.utils.safestring import  mark_safe

register = template.Library()


@register.filter #이런것은 애너테이션 이라고 한다.
def sub(value, arg):
    return value - arg
# 기존의 값인 value에서 입력받은 값인 arg를 빼서 반환한다.
 # 더하기 필터는 있지만 빼기 필터는 없으므로 빼기 필터를 만들어주는 과정이다.

# 마크다운 함수
@register.filter
def mark(value):
    extensions = ['nl2br', 'fenced_code'] # extensions => 마크다운 확장도구
    # 'nl2br' => 줄바꿈 문자를 <br>테그로 바꿔줌. (엔터 한 번만 눌러도 줄바꿈으로 인식함)
    # 'fenced_code' => 마크다운의 소스 코드 표현
    # 마크다운 확장 기능 문서: python-markdown.github.io/extensions 참고

    return mark_safe(markdown.markdown(value, extensions = extensions))
# markdown 모듈과 mark_sage 모듈을 이용해 문자열을 HTML코드로 반환한다.