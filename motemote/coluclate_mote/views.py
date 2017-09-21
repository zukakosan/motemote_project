from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from api import mote, twitter_api


def index(request):
    return render(request, 'coluclate_mote/index.html')


def result(request):
    content = {}

    if request.method == 'POST':
        screen_name = request.POST['screen_name']
        screen_name = screen_name.replace('@','')

        if not __is_exist_user(screen_name):
            return redirect('coluclate_mote:index')

        content['screen_name'] = screen_name
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


def __is_exist_user(screen_name):
    params = {
        "screen_name": screen_name,
        "count": 1,
        "include_user_entities": True,
    }
    req = twitter_api.get_instance("followers/list.json", params=params)

    if req.status_code != 200:
        return False
    else:
        return True


def how(request):
    return render(request, 'coluclate_mote/how.html')
