from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib import messages

from api import mote
from api import nega_posi,np
from coluclate_mote.form import TwitterAcountForm
import json

def index(request):
    content = {}
    form = TwitterAcountForm(auto_id=False)
    content['form'] = form
    return render(request, 'coluclate_mote/index.html', content)

def result(request):
    content = {}
    if request.method == 'POST':
        form = TwitterAcountForm(request.POST)
        if not form.is_valid():
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('/coluclate_mote/index#top_form')
        screen_name = form.data['screen_name'].replace('@','')
        content['screen_name'] = screen_name
        return render(request, 'coluclate_mote/result.html',content)
    else:
        raise Http404

def call_mote_api(request):
    if request.method == 'POST':
        params = json.loads(request.body.decode('utf-8'))
        screen_name = params['screen_name']
        result = mote.calc_mote(screen_name)
        result_np = np.get_tweet(screen_name)
        tweet_count_dev = np.get_tweetCount_dev(screen_name)
        print("ポジティブ偏差値は : "+ str(result_np['nega_posi_dev']))
        print("いいね数偏差値は : " + str(result_np['favo_dev']))
        print("tweet数偏差値は : "+str(tweet_count_dev))
        score = result['score']
        result['score'] = int(score * 100)
        response = json.dumps({'result': result})
        return HttpResponse(response, content_type='application/json')
    else:
        raise Http404

def how(request):
    return render(request, 'coluclate_mote/how.html')
