from django.urls import path, re_path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # все посты
    path('', views.feed, name='posts_feed'),
    # вход
    path('sign_in', views.sign_in, name='sign_in'),
    # регистрация
    path('sign_up', views.sign_up, name='sign_up'),
]