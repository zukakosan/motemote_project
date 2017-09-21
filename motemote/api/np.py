from api import nega_posi
import numpy as np
from api import twitter_api
from requests_oauthlib import OAuth1Session
from collections import defaultdict
import json

CK = '3rJOl1ODzm9yZy63FACdg'
CS = '5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8'
AT = '333312023-6dTniMxvwlQG8bATKNYWBXaQkftz9t4ZjRBt7BWk'
AS = 'LQ8xXBTTN8F8CHQv9oDAqsGJFeexdnFf2DFzn3EzGH2L8'

twitter = OAuth1Session(CK, CS, AT, AS)

def get_usid(scname):
    url = "https://api.twitter.com/1.1/users/show.json"
    # とくにパラメータは無い
    params = { "screen_name" : scname}
    # OAuth で GET
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.get(url, params = params)
    n = 0
    if req.status_code == 200:
        timeline2 = json.loads(req.text)
        print(timeline2["id"])
        return timeline2["id"]
    else:
        return 0

def get_tweet(usid):
    tweet_list=[]
    # タイムライン取得用のURL
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?count=300"
    # とくにパラメータは無い
    params = { "user_id" : usid}
    # OAuth で GET
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.get(url, params = params)
    n = 0
    # print(users["id_str"])
    if req.status_code == 200:
        # レスポンスはJSON形式なので parse する
        timeline = json.loads(req.text)
        # 各ツイートの本文を表示
        print(len(timeline))
        for tweet in timeline:
            if '@' not in tweet["text"]:
                tweet_list.append(tweet["text"])
                #print(tweet["text"])
            if len(tweet_list)==100:
                break
        return tweet_list
#         print(tweet_list)
    else:
        # エラーの場合
        print ("Error: %d" % req.status_code)
        return 0

def calc_score(tweet_list):
    score=0
    sum_score=0
    sc_list=[]
    for idx,tweet in enumerate(tweet_list):
#         print(idx)
        tw1=nega_posi.JudgeClass(tweet)
        tw1.make_wlist()
        score_dict=tw1.make_dict()
        tw1.make_judge_list()
        score=tw1.calc_score(score_dict)
        sum_score+=score
        sc_list.append(score)
    if len(tweet_list) == 0:
        return 0
    else:
        max_idx=search_max_idx(sc_list)
        for i,idx in enumerate(max_idx):
            print("positive "+str(i+1)+"位: "+str(tweet_list[idx]))
        min_idx=search_min_idx(sc_list)
        for i,idx in enumerate(min_idx):
            print("negative "+str(i+1)+"位: "+str(tweet_list[idx]))
        print(max_idx)
        print(min_idx)
        print("全体平均"+str(sum_score/len(tweet_list)))
        return sum_score/len(tweet_list)

def search_max_idx(sc_list):
    my_array=np.array(sc_list)
    #探す対象リスト:my_arrayはnumpy
    #例:上位3件
    K = 3
    # ソートはされていない上位k件のインデックス
    unsorted_max_indices = np.argpartition(-my_array, K)[:K]
    # 上位k件の値
    y = my_array[unsorted_max_indices]
    # 大きい順にソートし、インデックスを取得
    max_indices = np.argsort(-y)
    # 類似度上位k件のインデックス
    max_k_indices = unsorted_max_indices[max_indices]
    return max_k_indices

def search_min_idx(sc_list):
    my_array=np.array(sc_list)
    my_array=my_array*(-1)
    #探す対象リスト:my_arrayはnump
    #例:上位3件
    K = 3
    # ソートはされていない上位k件のインデックス
    unsorted_max_indices = np.argpartition(-my_array, K)[:K]
    # 上位k件の値
    y = my_array[unsorted_max_indices]
    # 大きい順にソートし、インデックスを取得
    max_indices = np.argsort(-y)
    # 類似度上位k件のインデックス
    max_k_indices = unsorted_max_indices[max_indices]
    return max_k_indices

def calc_dev(score,ave,std):
    return (50+10*(score-ave)/std)
