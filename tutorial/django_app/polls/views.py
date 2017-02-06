from django.http import HttpResponse
from django.shortcuts import render

from .models import Question
    # 모델부터 템플릿까지  배포하기 제외

def index(request):
    # 스텁메소드
    # 아직 개발되지 않은 코드를 임시로 대체하는 역할
    # 테스트코드.
    # ret = 'Q1 Q2 Q3'
    # return HttpResponse(ret)

    # pub_date 칼럼(필드)를 기준으로 내림차순 정렬한 결과를 latest_question_list에 할당
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {
        'latest_question_list': latest_question_list,
    }
    ## shortcut을 이용해 짧게 처리
    # polls/index.html 템플릿을 이용해서
    # request, context 객체를 이용해 HttpResponse를 반환
    return render(request, 'polls/index.html', context)

    # # 템플릿 로더를 이용해서 'polls/index.html'에서 템플릿파일을 가져온다
    # template = loader.get_template('polls/index.html')
    #
    # # 템플릿 파일에 전달할 context 객체를 정의
    # context = {
    #     # latest_question_list 라는 키에 값을 할당, 해당 키로 템플릿에서 사용가능하다.
    #     'latest_question_list': latest_question_list,
    # }
    # # 템플릿에 context와 request 객체를 사용해서 render해준 결과를 돌려줌
    # return HttpResponse(template.render(context, request))


    # # 돌려줄 문자열을 작성
    # output = ', '.join([q.question_text for q in latest_question_list])
    #
    # output2 = ''
    #
    # # 마지막 콤마를 빼기 위해서 enumerate로 활용할 수 있다
    # for q in latest_question_list:
    #     output2 += q.question_text + ', '
    # output2 = output2[:-2]
    #
    # return HttpResponse(output)
    #


def detail(request, question_id):
    return HttpResponse("You're looking at question {}".format(question_id))


def results(request, question_id):
    response = "You're looking at the results of question {}."
    return HttpResponse(response.format(question_id))


def vote(request, question_id):
    return HttpResponse("You're voting on question {}.".format(question_id))
