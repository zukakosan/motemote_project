from django.shortcuts import render,redirect
from django.http import Http404, HttpResponse
from api import mote


def index(request):
    return render(request, 'coluclate_mote/index.html')


def result(request):
    content = {}

    if request.method == 'POST':
        content['screen_name'] = request.POST['screen_name']
        return render(request, 'coluclate_mote/result.html',content)
    else:
        raise Http404


def call_mote_api(request):
    import json

    if request.method == 'POST':
        params = json.loads(request.body.decode('utf-8'))
        screen_name = params['screen_name']
        print(type(screen_name))
        print(screen_name)
        screen_name=screen_name.replace('@','')
        print(screen_name)
        result = mote.calc_mote(screen_name)
        if result is None:
            return redirect('http://127.0.0.1:8000/coluclate_mote/index','アカウント名が見つかりませんでした')

        score = result['score']
        result['score'] = int(score * 100)
        response = json.dumps({'result': result})
        return HttpResponse(response, content_type='application/json')
    else:
        raise Http404
