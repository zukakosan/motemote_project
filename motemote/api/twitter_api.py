#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session

BASEURL = 'https://api.twitter.com/1.1/'

CK = '3rJOl1ODzm9yZy63FACdg'
CS = '5jPoQ5kQvMJFDYRNE8bQ4rHuds4xJqhvgNJM4awaE8'
AT = '333312023-6dTniMxvwlQG8bATKNYWBXaQkftz9t4ZjRBt7BWk'
AS = 'LQ8xXBTTN8F8CHQv9oDAqsGJFeexdnFf2DFzn3EzGH2L8'


def get_instance(rest_url, params):
    url = BASEURL + rest_url
    print(url)
    twitter = OAuth1Session(CK, CS, AT, AS)
    return twitter.get(url, params=params)
