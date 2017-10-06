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

def get_tweet(screen_name):
    tweet_list=[]
    favolist=[]
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json?count=300"
    params = {"screen_name" : screen_name}
    twitter = OAuth1Session(CK, CS, AT, AS)
    req = twitter.get(url, params = params)
    n = 0
    if req.status_code != 200:
        return {
            'status': req.status_code,
            'reason': req.reason
        }
    else:
        timeline = json.loads(req.text)
        print(len(timeline))
        for tweet in timeline:
            if '@' not in tweet["text"]:
                tweet_list.append(tweet["text"])
                favolist.append(tweet["favorite_count"])
            if len(tweet_list)==100:
                break
        favo = sum(favolist)/len(favolist)
        favo_ave = 1.76596070695
        favo_std = 5.3013228418991245
        favo_dev = calc_dev(favo,favo_ave,favo_std)

        nega_posi_score = calc_score(tweet_list)
        nega_posi_ave = -0.3003982968868934
        nega_posi_std = 0.06567610108001085
        nega_posi_dev = calc_dev(nega_posi_score,nega_posi_ave,nega_posi_std)
        return  {
            "favo_dev": favo_dev,
            "nega_posi_dev": nega_posi_dev,
        }

def get_tweetCount_dev(screen_name):
    url = "https://api.twitter.com/1.1/users/show.json"
#     url = "https://api.twitter.com/1.1/statuses/mentions_timeline.json"
    favolist = []
    params = {
        "screen_name": screen_name,
        "include_entities": True,
    }
    req = twitter.get(url, params=params)
    result_tC = json.loads(req.text)
    tweet_count = result_tC['statuses_count']
    tweet_count_ave = 2969.449438202247
    tweet_count_std = 2765.3002952842094
    tweet_count_dev = calc_dev(tweet_count,tweet_count_ave,tweet_count_std)
    return tweet_count_dev

def calc_score(tweet_list):
    score=0
    sum_score=0
    sc_list=[]
    for idx,tweet in enumerate(tweet_list):
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
        print("全体平均"+str(sum_score/len(tweet_list)))
        return sum_score/len(tweet_list)

def search_max_idx(sc_list):
    my_array=np.array(sc_list)
    K = 3
    unsorted_max_indices = np.argpartition(-my_array, K)[:K]
    y = my_array[unsorted_max_indices]
    max_indices = np.argsort(-y)
    max_k_indices = unsorted_max_indices[max_indices]
    return max_k_indices

def search_min_idx(sc_list):
    my_array=np.array(sc_list)
    my_array=my_array*(-1)
    K = 3
    unsorted_max_indices = np.argpartition(-my_array, K)[:K]
    y = my_array[unsorted_max_indices]
    max_indices = np.argsort(-y)
    max_k_indices = unsorted_max_indices[max_indices]
    return max_k_indices

def calc_dev(score,ave,std):
    return (50+10*(score-ave)/std)
