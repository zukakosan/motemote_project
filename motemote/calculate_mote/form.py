# coding: utf-8
import re

from django import forms
from django.core.exceptions import ValidationError

from api import twitter_api


def validate_screen_name(screen_name):
    if not __is_vaild_screen_name(screen_name):
        raise ValidationError(
            "有効なアカウント名を入力して下さい。"
        )
    elif not __is_exist_user(screen_name):
        raise ValidationError(
            "このアカウントは存在しません。"
        )

def validate_user_protect(screen_name):
    if __is_protected_user(screen_name):
        raise ValidationError(
            "このアカウントは鍵がかかっています。鍵を外してご利用下さい。"
        )


def __is_exist_user(screen_name):
    params = {"screen_name": screen_name}
    req = twitter_api.get_instance("users/show.json", params=params)

    if '@' in screen_name:
        screen_name = screen_name[1::]
    if req.status_code != 200:
        return False
    else:
        return True

def __is_vaild_screen_name(screen_name):
    """
    有効なスクリーン名を入力しているかをboolean型で返す

    - 15文字以内か否か
    - アルファベットと数字とアンダーバーで構成されているか
    """
    if '@' in screen_name:
        screen_name = screen_name[1::]
    if len(screen_name) > 15:
        return False
    elif not re.match(r'^([a-zA-Z0-9_]+)$', screen_name):
        return False

    return True

def __is_protected_user(screen_name):
    params = {"q": screen_name, 'page':1, 'count':10}
    req = twitter_api.get_instance("users/search.json", params=params)

    protected = False
    for f in req.json():
        if f['screen_name']  == screen_name:
            protected = f.get('protected', False)
    return protected


class TwitterAcountForm(forms.Form):

    screen_name = forms.CharField(
        label='',
        required=True,
        error_messages = {'required': 'Twitterアカウント名を入力して下さい。'},
        widget=forms.TextInput(attrs={
            'class' : 'tw_name',
            'placeholder': '＠UserName',
            'onkeydown': 'go();'
            }),
        validators=[validate_screen_name, validate_user_protect]
        )
