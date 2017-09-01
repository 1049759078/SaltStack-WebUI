from django.conf.urls import url, include
from hostlist import views

urlpatterns = [
    url(r'^asset/get_hostasset/$', views.get_hostasset, name='get_hostasset'),
    url(r'^asset/idc_list/$', views.idc_list, name='idc_list'),
    url(r'^asset/host_list/$', views.host_list, name='host_list'),
    url(r'^asset/hostasset_list/(?P<ip>[0-9.]+)/$', views.hostasset_list, name='hostasset_list'),
]