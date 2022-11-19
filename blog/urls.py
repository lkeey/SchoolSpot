from django.urls import path, re_path
from . import views
from django.contrib.auth.decorators import login_required

from .views import (
    UsertListView, PostDetailtView,
) 

urlpatterns = [
    # все посты
    path('', views.feed, name='posts_feed'),
    # вход
    path('sign_in', views.sign_in, name='sign_in'),
    # регистрация
    path('sign_up', views.sign_up, name='sign_up'),
    # профиль пользователя в аккаунте
    path('my_profile', UsertListView.as_view(), name='student_profile'),   
    # добавление постов
    path('create', views.post_create, name='create_post'),
    # представление одного поста
    path('<int:pk>/detail', PostDetailtView.as_view(), name='post_detail'),   

]