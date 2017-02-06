### 간단한 폼 만들기

detail.html을 생성하고 다음 구문을 작성한다. 

> templates/polls/detail.html

```html
<h1>{{ question.question_text }}</h1>

{% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}

<form action="{% url 'polls:vote' question.id %}" method="post">
{% csrf_token %}
{% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}" />
    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br />
{% endfor %}
<input type="submit" value="Vote" />
</form>
```

![pic6](https://s27.postimg.org/ccvffbu77/pic6.png)

코드의 실행예제이다. 코드의 전반적인 내용은 프로그래밍 언어를 조금 배운 사람이라면 감을 쉽게 잡을 수 있다. `polls:vote`는 polls의 urls.py에서 vote라는 name을 가진 url을 참조한다. for 루프 반복 횟수만큼 radio버튼이 생길 것이며 각각의 name이 choice라는 것은 누군가 라디오 버튼 하나를 선택하고 폼을 제출하면 폼은 POST 데이터 choice=#를 전송한다는 뜻이다.  
post로 보내는 이유는 현재 폼이 서버의 데이터를 변경할 예정이기 때문에 get이 아닌 post를 사용한다. `{% csrf_token %}`는 보안에 관련된 명령어이다. 

vote view를 구현해보자 

> polls/views.py

```python
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Choice, Question
# ...
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 설문 폼을 다시 표시합니다.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
```
기본구조는 다른 view와 같다. question은 get_object_or_404함수로 객체를 받아온다. 만약 라디오 버튼에 선택을 했다면 else: 로 가기 때문에 votes 카운트를 올려주고 저장한다. 그리고 바로 결과화면을 보여주는데 이 때 HttpResponseRedirect로 반환한다. 제출하자마자 처리를 해주어야 사용자가 뒤로가기 버튼을 클릭했을 때 폼이 두 번 제출되는 현상을 방지한다.  
reverse함수는 `/polls/3/results/` 문자열을 반환한다. 따라서 전환된 URL이 `results` view로 이동시켜준다.  

results를 구현해보자. 

```python
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
```
detail view와 거의 비슷하다. 

results.html을 구현한다. 
```
<h1>{{ question.question_text }}</h1>

<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
{% endfor %}
</ul>

<a href="{% url 'polls:detail' question.id %}">Vote again?</a>
```
question을 참조하고 있는 choice_set을 다 순회하면서 votes 값을 출력시켜준다.  
마지막에 Vote again?이라는 버튼을 누르면 다시 detail view로 보내져서 투표를 할 수 있게 된다. 

-

### 제너릭 뷰 사용하기: 코드는 적을수록 좋다
앞서 구현한 view들은 코드의 중복이 많다.   
뷰들은 데이터를 불러오고 템플릿을 로드하여 템플릿에 데이터를 채워 반환한다. 일반적인 이 시나리오를 제너릭 뷰를 통해 간결하게 처리할 수 있다. 

1. URLconf를 변환한다.
2. 몇몇 낡고 불필요한 뷰를 삭제한다.
3. 장고 제너릭 뷰에 기반한 새 뷰를 도입한다.

위의 루틴을 따라가면 코드가 간결해진다.  

### #1. URLconf 수정하기
> polls/urls.py

```python
from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
```
detail, result view의 url에서 `<question_id>`가 `<pk>`로 변경되었다. 

### #2. 뷰 수정하기 

기존의 낡은 index, detail, results 뷰를 제거하고 장고 제너릭 뷰를 사용한다. 

> polls/views.py

```python
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    ... # same as above, no changes needed.
```
generic view는 이것만의 기본 템플릿을 제공한다. DetailView의 경우 `<app name>/<model name>_detail.html`가 기본 템플릿이다. 하지만 명시적으로 template_name='polls/detail.html'라고 지정했기 때문에 이 템플릿을 사용한다. 이는 다른 뷰에서도 마찬가지로 동작한다. 

각 generic view는 어떤 모델을 기반으로 동작해야하는지 알아야 하기 때문에 model을 명시적으로 입력해준다. Question 모델을 사용할 경우 context 변수를 자동적으로 모델 이름으로 사용한다. question을 context에 따로 입력해주지 않아도 된다. 그리고 위의 url에서 그룹이름을 `<pk>`로 변경했는데 이는 generic view가 기본키의 이름을 pk로 간주하기 때문이다.  

ListView의 경우 자동으로 생성되는 컨텍스트 변수가 question_list이다. 그래서 context_object_name 속성을 이용해 question_list가 아니라 latest_question_list를 사용하겠다고 지정한다. 

> ListView는 자동으로 생성되는 컨텍스트 변수가 question_list???  
