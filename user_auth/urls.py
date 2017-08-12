from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', auth_views.login, {'template_name':'user_auth/index.htm'}, name='index'),
    url(r'^register', views.register, name='register'),
    url(r'^test', views.test, name='test'),
]
