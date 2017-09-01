from django.conf.urls import url, include
from saltauth import views

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^account/logout/$', views.acc_logout, name = 'logout'),
    url(r'^account/login/$', views.acc_login, name = 'login'),
    url(r'^account/change_pwd/$', views.change_pwd, name = 'change_pwd')
]