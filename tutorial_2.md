### 데이터베이스 설정

settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
디폴트 ENGINE으로 다른 것도 있지만 sqlite를 쓰기 때문에 이 설정 그대로 유지하면 된다.  

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls',
]
```
INSTALLED_APPS에 polls를 추가한다.  

앱을 사용하기 전에 데이터베이스에 테이블을 생성해야 한다.  
```
$ python manage.py migrate
```
migrate 명령은 INSTALLED_APPS설정을 확인해, mysite/settings.py 파일의 데이터베이스 설정과 앱의 데이터베이스 마이그레이션에 따라, 필요한 데이터베이스 테이블을 생성한다. 

-

### 모델 만들기

poll이라는 설문에는 `질문`과 `선택지`가 있기 때문에 이를 각각 `Question`과 `Choice` 모델로 구현한다.  

> polls/models.py

```python
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```
각 클래스는 models.Model을 상속받아 모델로 구현된다. 각 모델은 필드를 구성했는데 이는 매우 직관적인 표현으로 이루어져 있다.  
CharField(max_length=200)는 최대길이가 200인 문자열을 말하고 IntegerField(default=0)은 디폴트값이 0인 정수형 변수를 말한다.

ForeignKey는 각 Choice가 하나의 Question과 연계된다고 장고에게 알려주는 것이다.  

모델에 변경사항이 발생하면 이를 django한테 알려야 한다. 

```
$ python manage.py makemigrations polls

#결과
Migrations for 'polls':
  polls/migrations/0001_initial.py:
    - Create model Choice
    - Create model Question
    - Add field question to choice
```
변경사항들이 나열된다. 

makemigrations 말그대로 migrations을 만든 상태이다. 아직 migrate는 하지 않았기 때문에 이를 명령해준다. 

```
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, polls, sessions
Running migrations:
  Rendering model states... DONE
  Applying polls.0001_initial... OK
```
migrate는 아직 적용되지 않은 migration들을 모두 가져와 데이터베이스에 적용시킨다.  

데이터베이스를 일일이 수정하지 않아도 된다는 가장 큰 장점이 있기 때문에 개발속도를 높일 수 있다. 

-

### API 써보기

파이썬 shell을 이용하여 데이터베이스 API를 직접 사용해본다.  
```
$ python manage.py shell
```
shell을 불러온다.

```python
>>> import django
>>> django.setup()
```
장고를 추가한다.  

```python
>>> from polls.models import Question, Choice
>>> Question.objects.all()
<QuerySet []>
```
구현해두었던 모델 클래스를 가져와서 출력해봐도 아직 값을 입력하지 않았기 때문에 아무것도 나오지 않는다.  

```python
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())
>>> q.save()
```
Question 모델에 데이터를 하나 만들고 저장한다.  

```python
>>> q.id
1
>>> q.question_text
"What's new?"
>>> q.pub_date
datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=<UTC>)
```
id값은 자동적으로 입력되기 때문에 1이 출력되고 다른 값도 직접 접근하여 출력해볼 수 있다.  

```python
>>> q.question_text = "What's up?"
>>> q.save()
```
값을 직접 변경하여 저장할수도 있다. 

>polls/models.py

```python
from django.db import models

class Question(models.Model):
    # ...
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    # ...
    def __str__(self):
        return self.choice_text
```
객체를 직접 호출했을 때 객체타입정보가 출력되는 것이 아니라 실제 값이 출력되도록 `__str__`을 지정해주는 것이 관례이다.  


-

### 관리자 페이지

관리자 페이지에서 사용할 계정을 설정한다.  

```
$ python manage.py createsuperuser

Username: admin

Email address: admin@example.com

Password: **********
Password (again): *********
Superuser created successfully
```
Username, Email, Password를 차례대로 입력하면 계정이 생성된다.  

```
$ python manage.py runserver
```
서버를 시작하고 관리자 페이지로 이동해본다.  

```
http://127.0.0.1:8000/admin/
```
![admin](https://docs.djangoproject.com/en/1.10/_images/admin01.png)

관리자 페이지 로그인 화면에서 생성했던 계정과 비밀번호를 입력한다.  

![admin2](https://docs.djangoproject.com/en/1.10/_images/admin02.png)

django.contrib.auth에서 기본적으로 제공해주는 Groups와 Users 외에 Polls앱을 통해 생성한 모델도 추가한다.  

>polls/admin.py

```python
from django.contrib import admin

from .models import Question

admin.site.register(Question)
```
admin site에 Question을 register하는 구문이다.  

![admin3](https://docs.djangoproject.com/en/1.10/_images/admin03t.png)

Question 모델이 추가되었다. Questions을 클릭해서 들어가면 목록과 추가, 수정, 삭제할 수 있는 옵션이 있다. 그리고 객체들의 변경이력도 확인할 수 있다.  
