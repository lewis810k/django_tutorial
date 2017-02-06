### 애플리케이션의 외형과 느낌 개별화하기

polls 디렉터리 안에 이름이 static인 디렉터리를 만든다. css나 image 파일등은 static으로 처리한다. 

> polls/static/polls/style.css
```
li a {
    color: green;
}
```
style.css를 만들고 color값을 지정해본다. 

> polls/templates/polls/index.html
```
{% load static %}

<link rel="stylesheet" type="text/css" href="{% static 'polls/style.css' %}" />
```
{% load static %}은 static의 절대경로를 반환해준다. 따라서 {% static 'polls/style.css' %}은 `static/polls/style.css`경로로 파일을 로드한다. 

-

### 배경이미지 추가하기 

```
body {
    background: white url("images/background.jpg") no-repeat right bottom;
}
```
static/polls/images 디렉토리 내부에 background.jpg 파일을 저장하고 css에 위와 같이 적용할 수 있다. 

![pic](https://s29.postimg.org/bffog1pif/pic8.png)

색깔과 이미지가 적용된 것을 확인할 수 있다. 
