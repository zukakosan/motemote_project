from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib import messages

from api import mote
from api import nega_posi,np
from calculate_mote.form import TwitterAcountForm
import json

def index(request):
    content = {}
    form = TwitterAcountForm(auto_id=False)
    content['form'] = form
    return render(request, 'calculate_mote/index.html', content)

def result(request):
    content = {}
    if request.method == 'POST':
        form = TwitterAcountForm(request.POST)
        if not form.is_valid():
            for error in form.errors.values():
                messages.error(request, error)
            return redirect('/calculate_mote/index#top_form')
        screen_name = form.data['screen_name'].replace('@','')
        content['screen_name'] = screen_name
        return render(request, 'calculate_mote/result.html',content)
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
        nega_posi_dev = int(result_np['nega_posi_dev'])
        favo_dev = int(result_np['favo_dev'])
        tweet_count_dev = int(tweet_count_dev)

        result['score'] = int(score * 100)
        print("sex数偏差値は : "+str(result['sex']))
        if result['sex'] == 2:
            if tweet_count_dev < 50 and favo_dev < 50 and nega_posi_dev >= 50:
                result['illust_img'] = '/static/img/illust/men01.jpg'
                result['dev_text'] = '特に特徴がない君'
                result['dev_comment'] = 'ツイート数は周りに迷惑をかけないようにやや控えめみたいだけど、ツイートは特に面白くないため存在感は薄いかも。誕生日でもみんなに忘れられがちな君は、女の子からリプがきたりお気に入りされたりすると意識しちゃうタイプかも！？'

            elif tweet_count_dev >= 50 and favo_dev < 50 and nega_posi_dev >= 50:
                result['illust_img'] = '/static/img/illust/men02.jpg'
                result['dev_text'] = 'ウェイ系大学生'
                result['dev_comment'] = '明るく活発な君は、ちょっとツイートがうるさい傾向にあるみたい。Twitter上ではパリピでウェイ系大学生みたいに思われているかも。だけど現実は意外と地味で自分が地味でない事、友達がいるアピールをしたい寂しがり屋さんだったりして...'

            elif tweet_count_dev < 50 and favo_dev >= 50 and nega_posi_dev >= 50:
                result['illust_img'] = '/static/img/illust/men03.jpg'
                result['dev_text'] = '勘違いホストな君'
                result['dev_comment'] = '更新頻度は少なめなのに、ツイートすればお気に入りがいっぱいくる君は自分を愛してやまないホストみたい。女子からも注目されているから、ついつい勘違いしちゃいがちかも。実はツイートする前にメモ帳で何度も書き直してたり！？'

            elif tweet_count_dev >= 50 and favo_dev < 50 and nega_posi_dev >= 50:
                result['illust_img'] = '/static/img/illust/men06.jpg'
                result['dev_text'] = 'うるさバンドマン'
                result['dev_comment'] = '元気なツイートをたくさんしてるのに、お気に入りが少ないのはなんでだろう？ツイートが多くて、もしかしたら女の子に暑苦しいくてうるさい騒音男に思われてるかも。うるさい男は疲れそう...クールな男を目指してみて！'


            elif tweet_count_dev < 50 and favo_dev < 50 and nega_posi_dev < 50:
                result['illust_img'] = '/static/img/illust/men05.jpg'
                result['dev_text'] = '犯罪者な君'
                result['dev_comment'] = 'たまにつぶやいたと思えば暗いツイートだったり、一言ツイートだったり...。女の子はほぼ見てないよ君のツイート。だってタイムラインにいないんだもん。でも他人のツイートはしっかり見てる君は変態で犯罪に走りそう...。周りからはちょっとやばいやつ認定されてるかも！？'

            elif tweet_count_dev >= 50 and favo_dev < 50 and nega_posi_dev < 50:
                result['illust_img'] = '/static/img/illust/men04.jpg'
                result['dev_text'] = '引きこもりオタクな君'
                result['dev_comment'] = '暗くて短文なツイートを連発でいつもタイムラインにいるね。うすうす気づいてたと思うけど、君はメンヘラだよ。お気に入りが欲しくてツイートを繰り返してるけど、口数が多いオタクみたい。男の子のメンヘラは罪でしかない！いっぺんTwitterアプリ消してみる？'

            else:
                result['illust_img'] = '/static/img/illust/nekama.jpg'
                result['dev_text'] = 'ネカマな君'
                result['dev_comment'] = '残念！君は男の子？それとも女の子？あ！もしかしてネカマでしょ？ごめんね、性別がはっきりしないからモテ偏差値は出せないよ...。ネットだとみんな本性表すって言うけど、これが君の本当の性別かもしれないね！異性のふりしてる君は相手の反応を見るのに好奇心旺盛で変態かも！？'

        elif result['sex'] == 1:

            if tweet_count_dev < 50 and favo_dev < 50 and nega_posi_dev >= 50:
                result['illust_img'] = '/static/img/illust/women01.jpg'
                result['dev_text'] = '特に特徴のない君'
                result['dev_comment'] = 'ツイート数は周りに迷惑をかけないようにやや控えめみたいだけど、ツイートは特に面白くないため存在感は薄いかも。誕生日でもみんなに忘れられがちな君は、男の子からリプがきたりお気に入りされたりすると意識しちゃうタイプかも！？'

            elif tweet_count_dev >= 50 and favo_dev < 50 and nega_posi_dev >= 50:
                result['illust_img'] = '/static/img/illust/women06.jpg'
                result['dev_text'] = 'クレイマーな君'
                result['dev_comment'] = 'ツイート数が多くて、いつもタイムラインにいるね。暇なのかな？周りから見たら、いつもタイムラインにいるうるさい人ってイメージかも。クレイマーみたい！知らず知らずにミュートされてたりフォロー外されてたりするかも！？'

            elif tweet_count_dev >= 50 and favo_dev < 50 and nega_posi_dev >= 50:
                result['illust_img'] = '/static/img/illust/women02.jpg'
                result['dev_text'] = 'ギャルビッチな君'
                result['dev_comment'] = '明るく活発な君は、ちょっとツイートがうるさい傾向にあるみたい。Twitter上ではギャルでビッチっぽく思われているかも。だけど現実は意外と地味で自分が地味でない事、友達がいるアピールをしたい寂しがり屋さんだったりして...。'

            elif tweet_count_dev < 50 and favo_dev >= 50 and nega_posi_dev >= 50:
                result['illust_img'] = '/static/img/illust/women03.jpg'
                result['dev_text'] = 'ぶりっ子な君'
                result['dev_comment'] = 'ここぞというイベントがあると可愛く盛れた自撮りをアップしてお気に入りを稼いでいるんじゃない？さえない男の子からモテて勘違いしちゃってる君、それみんな下心かもよ？ぶりっ子なところ少し抑えたら、周りからもっと好印象かも！？'

            elif tweet_count_dev < 50 and favo_dev < 50 and nega_posi_dev < 50:
                result['illust_img'] = '/static/img/illust/women05.jpg'
                result['dev_text'] = '悪霊な君'
                result['dev_comment'] = 'タイムラインで友達が楽しそうにしているのを指くわえて見てるでしょ？ツイート数も少ないし、たまにツイートしたと思えば暗いツイートだったり、一言ツイートだったり...。存在感がまるでないよ！悪霊になってるよ！たまには周りに生存確認をさせてあげて？'

            elif tweet_count_dev >= 50 and favo_dev < 50 and nega_posi_dev < 50:
                result['illust_img'] = '/static/img/illust/women04.jpg'
                result['dev_text'] = 'メンヘラかまちょな君'
                result['dev_comment'] = '暗くて短文なツイートを連発でいつもタイムラインにいるね。うすうす気づいてたと思うけど、君はメンヘラだよ。かまちょで寂しがり屋な君は男の子から面倒くさそうって思われてるかも。そんなに落ち込まずに元気出して！'

            else:
                result['illust_img'] = '/static/img/illust/nekama.jpg'
                result['dev_text'] = 'ネカマな君'
                result['dev_comment'] = '残念！君は男の子？それとも女の子？あ！もしかしてネカマでしょ？ごめんね、性別がはっきりしないからモテ偏差値は出せないよ...。ネットだとみんな本性表すって言うけど、これが君の本当の性別かもしれないね！異性のふりしてる君は相手の反応を見るのに好奇心旺盛で変態かも！？'

        else:
            print("エラー")

        response = json.dumps({'result': result})
        return HttpResponse(response, content_type='application/json')
    else:
        raise Http404

def system(request):
    return render(request, 'calculate_mote/system.html')

def team(request):
    return render(request, 'calculate_mote/team.html')
