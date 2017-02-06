from django.conf.urls import url

from . import views						#views의 모든 구성요소를 추가한다.

urlpatterns = [
    url(r'^$', views.index, name='index'), #url에 아무것도 추가되지 않았을 경우를 처리한다.
]