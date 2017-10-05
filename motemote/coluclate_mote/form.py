# coding: utf-8
from django import forms
from django.core.exceptions import ValidationError

from api import twitter_api


def validate_screen_name(screen_name):
    if not __is_exist_user(screen_name):
        raise ValidationError(
            '%(screen_name)s が見つかりません',
            params={'screen_name': screen_name},
        )


def __is_exist_user(screen_name):
    params = {"screen_name": screen_name}
    req = twitter_api.get_instance("users/show.json", params=params)

    if req.status_code != 200:
        return False
    else:
        return True


class TwitterAcountForm(forms.Form):
    screen_name = forms.CharField(
        label='',
        required=True,
        error_messages={'required': 'ツイッターアカウント名を入力してください'},
        widget=forms.TextInput(attrs={
            'class' : 'tw_name',
            'placeholder': 'ツイッターアカウント名'
            }),
        validators=[validate_screen_name]
        )
