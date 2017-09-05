from django.shortcuts import render
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
        result = mote.calc_mote(screen_name)

        score = result['score']
        result['score'] = int(score * 100)

        response = json.dumps({'result': result})
        return HttpResponse(response, content_type='application/json')
    else:
        raise Http404
