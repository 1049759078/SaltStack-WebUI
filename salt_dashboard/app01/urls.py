from django.conf.urls import url, include
from app01 import views

urlpatterns = [
    url(r'^key_list/$', views.salt_key_list, name='key_list'),
    url(r'^key_fun/$', views.salt_key_fun, name='key_fun'),
    # url(r'^key_list/$', views.salt_key_list, name='key_list'),
    # url(r'^key_accept/$', views.salt_accept_key, name='accept_key'),
    # url(r'^key_delete/$', views.salt_delete_key, name='delete_key'),
    url(r'^command/$', views.command, name='command'),

    url(r'^execute/$', views.execute, name='execute'),
    url(r'^execute_fun/$', views.execute_fun, name='execute_fun'),
    url(r'^result/$', views.result, name='result'),
    url(r'^jid_info/$', views.jid_info, name='jid_info'),
]