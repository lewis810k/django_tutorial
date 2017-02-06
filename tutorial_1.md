# 프로젝트 생성하기

디렉토리 이름을 tutorial2로 진행했습니다. 

프로젝트를 생성하기 위해서 Pycharm 터미널에서 다음 명령어를 입력한다. 
```
$ django-admin startproject mysite
```
![pic1](https://s30.postimg.org/3ucqp1moh/pic1.png)

빈 디렉토리였지만 manage.py, urls.py, wsgi.py, settings.py 등이 자동적으로 생성된 것을 확인할 수 있다. 


각 파일과 디렉토리의 역할은 다음과 같다. 

- 바깥쪽 mysite/  
	: 프로젝트를 담는 루트 디렉터리입니다. 장고 입장에서 이름은 별로 중요하지 않으므로 마음대로 바꿔도 됩니다.
- manage.py  
	: 다양한 방법으로 장고 프로젝트를 관리할 수 있는 명령행 유틸리티입니다. manage.py에 관한 세부 내용은 django-admin과 manage.py을 참조하십시오.
- 안쪽 mysite/  	
	: 프로젝트에서 사용하는 실제 파이썬 패키지입니다. 디렉터리 이름은 패키지 안에 있는 뭔가를 가져올 때 사용할 파이썬 패키지 이름(예: mysite.urls) 입니다.
- mysite/__init__.py  
	: 빈 파일입니다. 해당 디렉터리가 패키지라는 사실을 파이썬에게 알려 줍니다. 파이썬 초보라면 파이썬 공식 문서의 패키지 설명을 참조하십시오.
- mysite/settings.py  
	: 장고 프로젝트에 대한 설정과 구성 정보가 담긴 파일입니다. 설정에 관한 자세한 내용은 장고 설정을 참조하십시오.
- mysite/urls.py  
	: 장고 프로젝트에서 사용할 URL을 선언합니다. 사이트의 “목차(table of contents)”와 같습니다. URL에 관한 자세한 내용은 URL dispatcher를 참조하십시오.
- mysite/wsgi.py  
	: WSGI-호환 웹 서버를 위한 진입점(entry point)입니다. 세부 사항은 WSGI와 함께 배포하는 법을 참조하십시오.

출처 : [장고튜토리얼 1부](http://www.fastcampus.co.kr/coaching/docs/django-tutorial/intro/tutorial01/)

-

### 개발서버

```
$ python manage.py runserver
```
위의 명령어를 입력하여 프로젝트를 구동시킨다. 정상적인 동작이 되면 다음과 같은 메시지가 출력된다.  

```
August 26, 2016 - 15:50:53
Django version 1.10, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
디폴트 주소값으로 `http://127.0.0.1:8000/`가 설정된다.  

```
$ python manage.py runserver 8080
```
디폴트 포트값이 8000인데 직접 다른 포트번호를 입력할수도 있다.  

![pic2](https://s30.postimg.org/q7khbunm9/pic2.png)

정상적으로 동작했을 때 'It worked'라는 메시지를 확인할 수 있다.  

-

### 앱 만들기

이제까지 프로젝트를 만들었다면 앱을 생성해야한다.  

```
$ python manage.py startapp polls
```
![pic3](https://s24.postimg.org/8x25syqhh/pic3.png)

polls 디렉토리가 생성되고 여러 파일들이 자동으로 추가된다.  

-

### 첫번째 뷰 만들기

화면에 보여지는 뷰를 만드는 과정이다.  

>polls/views.py

```python
from django.http import HttpResponse  

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```
모든 뷰는 url과 매칭이 되어야 한다. polls 디렉토리에 urls.py 파일을 새로 생성하고 다음 코드를 추가한다.  

>polls/urls.py

```python
from django.conf.urls import url

from . import views						#views의 모든 구성요소를 추가한다. 

urlpatterns = [
    url(r'^$', views.index, name='index'), #url에 아무것도 추가되지 않았을 경우를 처리한다. 
]
```

메인의 urls.py도 수정해야한다.  
>mysite/urls.py

```python
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^polls/', include('polls.urls')),
    url(r'^admin/', admin.site.urls),
]
```
첫번째 url은 polls 앱과 관련된 url을 처리해준다.  
두번째 url은 관리자페이지에 대한 url을 처리한다.  

>**include()는 언제 사용할까?**  
다른 URL 패턴을 포함할 때는 항상 include()를 사용해야 합니다. admin.site.urls가 유일한 예외입니다.

뷰와 url이 설정되었기 때문에 다시 한 번 runserver명령을 실행한다. 
```
$ python manage.py runserver
```
`127.0.0.1:8000/polls/`주소를 따라가보면 다음과 같은 뷰가 나와야 정상이다.  

![pic4](https://s28.postimg.org/uacw9skvx/pic4.png)

-

urls()함수는 매개변수 4개를 취할 수 있다.  

```python
urls(regex, view, kwargs, name)
```
regex와 view는 필수이고 kwargs와 name은 선택적으로 사용된다.  

