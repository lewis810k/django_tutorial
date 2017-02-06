# 자동화된 테스트

테스트란 코드가 동작하는지 확인하는 간단한 루틴이다. 

- 테스트는 시간을 절약해준다. 
- 테스트는 문제를 찾을뿐만 아니라 예방도 한다.
- 테스트는 코드의 매력을 높입니다
- 테스트는 팀의 협업을 돕습니다

### 첫 테스트 작성하기

Question 모델에서 `Question.was_published_recently()` 메소드는 Question이 지난 24시간 내에 발행된 경우 True를 반환한다. 하지만 Question의 pub_date 필드가 미래인 경우도 (잘못된 값인) True를 반환한다. 

![img1](https://s27.postimg.org/3t86dswer/pic7.png)
pub_date가 30일 이후인 question 객체를 생성했는데 `was_published_recently()`함수의 출력값은 True가 나왔다. 미래 시간의 경우 상식적으로 True는 성립되지 않는다. 

-

### 테스트를 만들어 버그 드러내기
shell에서 매번 일일이 테스트를 진행하지 않고 테스트코드를 만들어서 버그를 발견할 수 있다. 

> polls/tests.py

```python
import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Question

class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        pub_date가 미래면 was_published_recently()는
        false를 반환해야 마땅합니다.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
```
future_question은 Question의 객체이며 미래 시간을 가지고 있다. 

-

### 테스트 실행

```
$ python manage.py test polls
```
테스트를 실행하면 FAILED가 나온다.   
self.assertIs 구문에서 미래 날짜를 가지는 변수를 넣을 경우 원하는 답은 False이다.

```
Traceback (most recent call last):
  File "/home/lewis/projects/django/tutorial/polls/tests.py", line 17, in test_was_published_recently_with_future_question
    self.assertIs(future_question.was_published_recently(), False)
AssertionError: True is not False
```
테스트 결과에서는 몇번줄에서 에러가 발생했는지도 알 수 있다. 

-

### 버그 수정
```python
def was_published_recently(self):
    now = timezone.now()
    return now - datetime.timedelta(days=1) <= self.pub_date <= now
```

문제가 생겼던 함수를 수정한다. pub_date가 현재시간값(now)보다 작아야 한다는 조건을 붙인다. 그렇게 되면 모든 미래 시간은 false로 처리된다. 이렇게 바꾸고 test를 다시 해보면 `OK`가 출력된다. 

더 디테일하게 테스트하려면 24시간 이전에 대해서 과거이기 때문에 최근인지에 대한 질문에는 False를 반환해야 하고 24시간 이내의 경우 True를 출력해야 한다는 테스트 함수를 구현할 수 있다. 

-

### 뷰 테스트

미래 시점에 있는 설문조사는 출력하지 않도록 한다.  

> polls/views.py

```python
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """가장 최근에 발행된 설문 5개를 반환합니다."""
        return Question.objects.order_by('-pub_date')[:5]
```
여기에서 get_queryset 함수를 수정한다. 

```python
def get_queryset(self):
    """
    (미래에 발행할 설문은 제외하고) 가장 최근에 발행된 설문 5개를 반환합니다
    """
    return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]
```
미래는 제외하고 현재시간을 포함하거나 이전의 자료만 반환한다.  
