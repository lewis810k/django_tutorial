# 환경설정

Ubuntu에서 진행하였습니다.

```
/home/<user_name>/projects/django/tutorial

pyenv virtualenv 3.4.3 django_tutorial_env
pyenv local django_tutorial_env
pyenv versions
```
tutorial이라는 폴더를 따로 만들고 pyenv 환경을 구성하고 로컬로 지정한다. 
환경설정의 자세한 내용은 [여기](https://github.com/LeeHanYeong/Fastcampus-WPS-4th/blob/master/Python/01.%20pyenv%2C%20virtualenv%2C%20iPython%20%EC%84%A4%EC%B9%98%20%EB%B0%8F%20%EC%84%A4%EC%A0%95.md)를 참고한다. 

```
pip install django==1.10
python -m django --version

1.10
```
tutorial 디렉토리에서 django의 최신버전을 설치하고 제대로 설치됐는지 확인한다.  

![1](https://s28.postimg.org/wekuf78vx/Screenshot_from_2017_02_06_01_00_18.png)

새로 만든 디렉토리를 Pycharm에서 로드하고 Project Interpreter를 세팅해준다.  

