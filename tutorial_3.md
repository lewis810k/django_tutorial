### 뷰 만들기

>polls/views.py

```python
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```
투표 어플리케이션에서는 다음과 같이 네 개 뷰가 존재한다. 

질문 “인덱스” 페이지(index) - 가장 최신의 몇몇 질문들을 보여줍니다.
질문 “세부” 페이지(detail) - 투표를 위한 폼과 함께 질문 내용을 보여주지만 결과는 보여주지 않습니다.
질문 “결과” 페이지(results) - 특정 질문에 대한 결과를 보여줍니다.
투표하기(vote) - 특정 질문에 대해 특정 선택을 할 수 있게 투표를 관리합니다.

요청받은 url에 따라 어떤 뷰가 보여질지 장고가 결정한다. 새로 설정한 뷰를 url 모듈과 연결해야 한다.  

>polls/urls.py

```python
from django.conf.urls import url

from . import views

    urlpatterns = [
        # ex: /polls/
        url(r'^$', views.index, name='index'),
        # ex: /polls/5/
        url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
        # ex: /polls/5/results/
        url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
        # ex: /polls/5/vote/
        url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    ]
```
/polls/5/ 형태의 요청이 들어오면 이에 해당되는 url을 정규표현식으로 매칭시킨다. views.detail과 매칭되기 때문에 뷰의 detail이 화면에 출력된다.  


```python
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)
```
detail 뷰는 request와 question_id를 매개변수로 취한다.  
```python
# ex: /polls/5/
url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
```
/polls/5/가 위의 정규표현식에 해당됐을 때 다음과 같이 요청된다.  
```python
detail(request=<HttpRequest object>, question_id='5')
```

-

생성 날짜에 따라 콤마로 분리되어 시스템에 저장된 최신 투표 질문 다섯 개를 보여주는 새로운 index()뷰는 다음과 같다.

>polls/views.py

```python
from django.http import HttpResponse
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
```
order_by에서 -pub_date로 처리했기 때문에 내림차순으로 정리된다. 그 중 상위 다섯개의 아이템을 출력한다.  
output이라는 변수에 문자열을 join으로 묶어서 return의 HttpResponse에 인자값으로 넘겨준다. output의 내용이 뷰에 출력될 것이다. 하지만 뷰를 수정하고 싶을 경우 파이썬 코드를 같이 수정해주어야 하기 때문에 뷰만 담당하는 템플릿을 따로 구현한다.  

![pic5](https://s23.postimg.org/vx9jf8tdn/pic5.png)

templates 디렉토리 내에 polls디렉토리를 새로 생성하고 여기에 index.html을 만든다.  

```
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```
index.html의 코드이다. 문법적인 부분은 조금 생략하고 흐름만 파악해보면, latest_question_list라는 변수에 내용이 있으면 for 루프를 실행하고 아니면 'No polls are available' 메시지를 출력한다. for 루프에는 latest_question_list 안의 데이터를 하나씩 불러오면서 링크 주소를 `/polls/{{ question.id }}`로 하는 `a tag`를 만든다. 그리고 `a tag`태그의 텍스트를 각 아이템의 text로 한다.  

> polls/views.py

```python
from django.http import HttpResponse
from django.template import loader

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
      return HttpResponse(template.render(context, request))
```
views.py가 수정되었다. 이전에 output 변수를 통해서 출력한 것과 달리 template 변수가 loader를 통해 `polls/index.html` 파일을 호출한다. index.html에 넘겨줄 변수를 context에 담고 템플릿과 변수를 렌더링하여 인자값으로 넘겨준다.  

-

### get_object_or_404()

> polls/views.py

```python
from django.shortcuts import render
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
```
render를 import하여 return에서 바로 호출하는 방법이다. render의 인자값으로 request, 템플릿, 필요한 변수객체를 사용한다. 이전 과정과 동작은 동일하지만 코드가 더 간결해졌다.  

만약 객체가 존재하지 않으면 뷰는 Http404 예외를 던진다. 

>>polls/views.py

```python
from django.shortcuts import get_object_or_404, render

from .models import Question
# ...
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
```
모델 클래스로부터 정보를 넘겨받을 때 내용이 존재하면 object로 받고 없으면 404예외를 던지도록 하는 구문이다. 관용적으로 `get_object_or_404`를 많이 사용한다. 


-

### 템플릿에 고정되어있는 URL을 제거하기

```
<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
```
이렇게 사용할 경우 해당 `a tag`는 `/polls/{{ question.id }}`에만 한정적으로 동작한다. 만약 관리자가 polls라는 경로를 바꾸고 싶다면 모든 polls를 바꿔야 하는 비효율이 생긴다.  

`urls.py`에서 줄 수 있는 name옵션을 통해 코드의 유연함을 살릴 수 있다.  
```
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
```
{% url 'detail' question.id %} 구문은 url 목록에서 name이 detail로 지정되어있는 url을 가져오도록 하고 그 뒤에 question.id 를 추가하도록 한다. 

```
url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
```
만약 투표 세부 뷰의 URL을 (polls/specifics/12/처럼) 다른 URL로 변경하고 싶다면,

```
url(r'^specifics/(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
```
템플릿에 고정시키는 방식 대신에 polls/urls.py에서 specifics만 추가하면 된다.  
name으로 매치시켜주기 때문에 {% url 'detail' question.id %}가 자동적으로 specifics를 추가해서 사용한다.  

-

### URL 이름을 이름영역으로 분리하기

polls 앱 이외에 여러 앱을 구동시킨다면 urls.py 또한 여러개가 되기 때문에 장고는 어떤 urls.py를 참조해야할지 정해야 한다.  

> polls/urls.py

```python
from django.conf.urls import url
from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
```
`app_name = 'polls'`를 추가하면 외부에서 참조할 때 사용할 수 있다.  

```
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
```
`{% url 'detail' question.id %}`는 모든 urls 중에 detail이라는 이름을 가진 url을 매칭시킨다. 하지만 `{% url 'polls:detail' question.id %}`는 특정 앱에(여기서는 polls) 있는 urls를 참조하기 때문에 구분할 수 있다.  







```













```
    
    
    
