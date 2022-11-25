from django.urls import path, re_path
from . import views
from django.contrib.auth.decorators import login_required

from .views import (
    UsertListView, PostDetailtView,
    LikekView, MarkView, CertificateView
) 

from .models import (
    PostLike,
)

urlpatterns = [
    # все посты
    path('<int:page>', views.feed, name='posts_feed'),
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
    # лайк поста
    path('post/<int:pk>/like/', LikekView.as_view(model=PostLike), name='like_post'),
    # like in detail
    path('<int:id>/post/<int:pk>/like/', LikekView.as_view(model=PostLike), name='like_post'),
    # add mark
    path('mark', MarkView.as_view(), name='add_mark'),
    # rating
    path('rating', views.rating, name='rating'),
    # create certificate
    path('<begin_date>/<end_date>/<student>/certificate', CertificateView.as_view(), name='add_certificate'),
    # add certificate
    path('<begin_date>/<end_date>/<student>/pdf', CertificateView.as_view(), name='add_certificate'),
    # show pdf
    path('<begin_date>/<end_date>/pdf', views.show_pdf, name='show_pdf'),
    # top posts
    path('top_posts', views.top_posts, name='top_posts'),
    # next page
    path("load_more/", views.loadMore, name="load_more"),
    # https://realpython.com/django-pagination/
    # https://www.youtube.com/watch?v=LoRcRUuxN1U
]