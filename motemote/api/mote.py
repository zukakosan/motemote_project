#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import math
import json
from api import twitter_api
import numpy as np
from sklearn.externals import joblib

MEAN = 0.5
VAR = 0.1
# 考慮するフォロワー 最大200
COUNT = 100


class RateCalculator():
    def __init__(self):
        api_dir_path = os.path.dirname(os.path.abspath(__file__))
        dump_dir_path = api_dir_path + '/dump'
        self.clf = joblib.load("{0}/clf.pkl".format(dump_dir_path))
        self.n_cv = joblib.load("{0}/name_cv.pkl".format(dump_dir_path))
        self.s_cv = joblib.load("{0}/screen_cv.pkl".format(dump_dir_path))
        self.d_cv = joblib.load("{0}/desc_cv.pkl".format(dump_dir_path))
        self.l_cv = joblib.load("{0}/loc_cv.pkl".format(dump_dir_path))

    def calc(self, response_text):
        followers = json.loads(response_text)

        features = []
        for f in followers["users"]:
            features.append(self.extract_feature(f))

        n_male = 0
        n_female = 0
        predicted = self.clf.predict(features)
        for p in predicted:
            if p == 1:
                n_male += 1
            else:
                n_female += 1
        return n_male, n_female

    def extract_feature(self, profile):
        print("Convert profile to feature")
        feature = []
        name = list(profile["name"])
        n_n_gram = gen_n_gram(name, 1)
        n_n_gram.extend(gen_n_gram(name, 2))
        n_n_gram.extend(gen_n_gram(name, 3))

        s_name = list(profile["screen_name"])[1:]
        s_n_gram = gen_n_gram(s_name, 1)
        s_n_gram.extend(gen_n_gram(s_name, 2))
        s_n_gram.extend(gen_n_gram(s_name, 3))

        desc = list(profile["description"])
        d_n_gram = gen_n_gram(desc, 1)
        d_n_gram.extend(gen_n_gram(desc, 2))
        d_n_gram.extend(gen_n_gram(desc, 3))

        loc = list(profile["location"])
        l_n_gram = gen_n_gram(loc, 1)
        l_n_gram.extend(gen_n_gram(loc, 2))
        l_n_gram.extend(gen_n_gram(loc, 3))

        feature.extend(
            n_gram2vec(self.n_cv, n_n_gram)
        )
        feature.extend(
            n_gram2vec(self.s_cv, s_n_gram)
        )
        feature.extend(
            n_gram2vec(self.d_cv, d_n_gram)
        )
        feature.extend(
            n_gram2vec(self.l_cv, l_n_gram)
        )
        feature.append(int(profile["protected"]))
        feature.append(np.log10(int(profile["followers_count"]) + 1))
        feature.append(np.log10(int(profile["friends_count"]) + 1))
        feature.append(np.log10(int(profile["statuses_count"]) + 1))
        feature.append(np.log10(int(profile["media_count"]) + 1))

        feature.append(
            int(profile["url"] is not None)
        )

        # if set pref language
        feature.append(
            int(profile["lang"] != "ja")
        )

        # リストを持っているかどうか
        feature.append(
            int(profile["listed_count"] != 0)
        )

        # 色を変えているかどうか 通常1DA1F2
        feature.append(
            int(profile["profile_link_color"] != "1DA1F2")
        )

        # 色を変えているかどうか 通常333333
        feature.append(
            int(profile["profile_text_color"] != "1DA1F2")
        )

        # 色を変えているかどうか 通常C0DEED
        feature.append(
            int(profile["profile_sidebar_border_color"] != "C0DEED")
        )

        feature.append(int(profile["contributors_enabled"]))
        feature.append(int(profile["is_translator"]))
        feature.append(int(profile["is_translation_enabled"]))
        feature.append(int(profile["profile_use_background_image"]))
        feature.append(int(profile["has_extended_profile"]))
        feature.append(int(profile["default_profile"]))
        feature.append(int(profile["default_profile_image"]))
        feature.append(int(profile["has_custom_timelines"]))
        feature.append(int(profile["can_media_tag"]))
        return feature


def gen_n_gram(lst, n, delim=" "):
    return [delim.join(
                (["<s>"] * (n - 1) + lst + ["</s>"] * (n - 1))[i: i + n]
            ) for i in range(len(lst) + n - 1)]


def n_gram2vec(lst, n_gram):
    print("Start: n-gram to vector")
    vec = np.zeros(len(lst))
    for n in n_gram:
        if n in lst:
            vec[lst.index(n)] += 1
    print("Finish: n-gram to vector")
    return vec


def calc_mote(screen_name):
    params = {
        "screen_name": screen_name,
        "count": COUNT,
        "include_user_entities": True,
    }
    req = twitter_api.get_instance("followers/list.json", params=params)
    calculater = RateCalculator()
    n_male, n_female = calculater.calc(req.text)

    params = {
        "screen_name": screen_name,
        "include_entity": True,
    }
    print(params)
    c_male = 0
    c_female = 0
    req = twitter_api.get_instance("users/lookup.json", params=params)
    user_profile = json.loads(req.text)
    if calculater.clf.predict(calculater.extract_feature(user_profile[0])) == [1]:
        rate = n_female / (n_male + n_female)

    else:
        rate = n_male / (n_male + n_female)

    return {
        "ratio": rate,
        "score": ((rate - MEAN) / math.sqrt(VAR)) * 0.1 + 0.5,
    }
