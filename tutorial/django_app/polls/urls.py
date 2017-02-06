from django.conf.urls import url

from . import views						#views의 모든 구성요소를 추가한다.

urlpatterns = [
    # /polls/
    url(r'^$', views.index, name='index'), #url에 아무것도 추가되지 않았을 경우를 처리한다.
    # /polls/5
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    # question_id값으로 인자를 넘긴다 view.py에서 각 뷰의 question_id로
]