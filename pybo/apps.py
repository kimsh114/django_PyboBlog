from django.apps import AppConfig


class PyboConfig(AppConfig): # 파이보 컨피그 클래스가 config/setting.py 파일의 INSTALLED_APPS 항목에 추가가 안되면 장고는 이 앱을 인식 못한다.
    name = 'pybo'
