from natto import MeCab
nm=MeCab()
import os
import math
import json
from api import twitter_api
import numpy as np
from sklearn.externals import joblib
from django.conf import settings

class JudgeClass :
    #初期化
    def __init__(self,tweet):
        self.tweet = tweet
        self.wlist = []#??
        self.judge_list=[]

    #nm.parseをtweetにかける.
    def make_wlist(self):
        wakati=nm.parse(self.tweet).split('\n')
        #print(wakati)
        for ws in wakati:
            ws=ws.split(',')
            self.wlist.append(ws)#インスタンスにappend

        #前処理マン
        for w in self.wlist:
            if '名詞' in w[0]:
                w[0]='名詞'
            elif '形容詞' in w[0]:
                w[0]='形容詞'
            elif '副詞' in w[0]:
                w[0]='副詞'
            elif '動詞' in w[0]:
                w[0]='動詞'
            else:
                w[0]=w[0]
        del self.wlist[len(self.wlist)-1]
        #print(self.wlist)

    #ネガポジ判定の対象となる単語を取り出す
    def make_judge_list(self):
        for word in self.wlist:
            if(word[6] != '*'):
                if ((word[0] == "名詞" ) or (word[0] == "形容詞") or (word[0] == "動詞") or (word[0] == "副詞")) :
                     self.judge_list.append(word[6]) #インスタンスにappend
        #print(self.judge_list)

    #点数付けのための辞書を作る
    def make_dict(self):
        os.chdir(os.getcwd())
        f = open(str(settings.BASE_DIR)+'/api/pn_ja.txt') #特殊な設定
        data1 = f.read()  # ファイル終端まで全て読んだデータを返す
        data1=data1.replace(':',',')
        f.close()
        lines=data1.split('\n')

        ##########点数辞書#############
        word_to_score=[]
        for line in lines:
            word=line.split(',')
            word_to_score.append(word)
        del word_to_score[55125]

        return word_to_score#どこかで代入しないといけない


    def calc_score(self,score_dict):
        ############点数計算############
        score=0
        wordcount=0
        min_score=1
        max_score=-1
        #setにして単語検索でもいける
        for word in self.judge_list:
            #print(word)
            for w_s in score_dict:
                if w_s[0]==word or w_s[1]==word :
                    score+=float(w_s[3])
                    #print('単語:'+w_s[3]+',合計:'+str(score))
                    wordcount+=1
                    break
        if(wordcount!=0):
            average=score/wordcount
            #print("平均"+str(average))
            return average
        else:
            return 0
        ###############################
