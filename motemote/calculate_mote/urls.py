from django.conf.urls import url
from calculate_mote import views

urlpatterns = [
    url(r'^index$', views.index, name='index'),
    url(r'^result$', views.result, name='result'),
    url(r'^call_mote_api$', views.call_mote_api, name='call_mote_api'),
    url(r'^how$', views.how, name='how'),
]
