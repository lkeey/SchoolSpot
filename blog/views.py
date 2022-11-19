from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView, CreateView, 
    DetailView, View,
)
from django.views.generic.edit import FormMixin
from django.urls.base import reverse_lazy

from .forms import PostCreateForm
from .models import (
        Student, Post,
    )

# Create your views here.

class UsertListView(ListView):
    # model in models.py
    model = Student

    # name of template
    template_name = 'blog/profile.html'

    # save data for cycle "for" in user_posts.html
    context_object_name = 'blog_post_user_list'

    def get_context_data(self, **kwargs):
        user = auth.get_user(self.request)
        student = Student.objects.get(user=user)

        context = {
            'user': user,
            'student': student,
        }

        return context

    def post(self, request, **kwargs):

        student = Student.objects.get(user=request.user)

        if request.FILES.get('image') == None:
            image = student.profile_img
            
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')

        bio = request.POST['bio']
        location = request.POST['location']

        student.profile_img = image
        student.bio = bio
        student.location = location
        student.save()

        return redirect('student_profile')    

class PostDetailtView(DetailView):
    model = Post

    template_name = 'blog/post_detail.html'
    context_object_name = 'post_detail'

    def get_success_url(self, **kwargs):
       
        return reverse_lazy('post_detail', kwargs={"pk":self.get_object().id})
    

@login_required(login_url='sign_in')
def feed(request):
    # show all posts

    context = {
        "user": request.user,
        "student": request.user.student,
        "all_posts": Post.objects.order_by('-date_created'),
    }

    return render(request, 'blog/posts_feed.html', context=context)

@login_required(login_url='sign_in')
def post_create(request):
    # добавление поста

    # если запрос POST. то тогда обрабатываем форму
    if request.method == 'POST':

        form = PostCreateForm(request.POST, request.FILES)
        
        # данные пост для заполнения формы
        if form.is_valid():

            new_post = form.save(commit=False)

            new_post.author = request.user

            new_post.image = request.FILES.get("image_upload")

            new_post.save()

            # return redirect(new_disccusion.get_absolute_url())
            data = {
                "post_detail": new_post,
            }

            messages.info(request, 'The post was created successfully')
            messages.success(request, 'Now all SchoolSpot users will see it')

            return redirect('post_detail', pk=new_post.pk)
            # return render(request, 'discussions/discussion_detail.html', data)

    
    # если get-запрос, то вернуть пустую форму
    formset = PostCreateForm()

    return render(request, 'blog/create.html', {'formset': formset})


def sign_in(request):
    # logging
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            messages.info(request, f'Hello, {user.username}')
            messages.success(request, 'We are glad to see you in SchoolSpot')

            data = {
                    # "all_posts": Post.objects.order_by('-date_created'),
                }

            # return render(request, 'discussions/posts_feed.html', data)
            return redirect('posts_feed')

        else:
            messages.warning(request, 'Data is invalid')

        
    # telegram_login_widget = create_callback_login_widget(bot_name, size=SMALL)

    context = {
        # 'telegram_login_widget': telegram_login_widget
    }

    return render(request, "blog/sign_in.html", context)

def sign_up(request):
    # registration

    if request.method == 'POST':
        
        username = request.POST['username']
        # email = request.POST['email']
        # telegram_id - default (0)
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:

            if len(username) >= 3 and len(password) >= 8:

                if User.objects.filter(username=username).exists():
                    messages.info(request, "Username was taken")

                else:

                    # create User
                    user = User.objects.create_user(
                        username=username,
                        # email=email,
                        password=password
                    )

                    user.save()

                    # redirect to settings
                    user_login = auth.authenticate(username=username, password=password)

                    auth.login(request, user_login)

                    # Create User's profile
                    user_model = User.objects.get(username=username)
                    
                    new_profile = Student.objects.create(
                        user=user_model, 
                        id_user=user_model.id,
                    )

                    new_profile.save()

                    messages.info(request, f'Hello, {user.username}')
                    messages.success(request, 'We are glad to see you in SchoolSpot')

                    data = {
                            # "all_posts": Post.objects.order_by('-date_created'),
                        }

                    # return render(request, 'discussions/posts_feed.html', data)
                    return redirect('posts_feed')
            else:
                messages.info(request, 'The username must be more than 2 characters and the password more than 7')

        else:
            messages.info(request, 'Password is not matching')
            return redirect('sign_up')

    # telegram_login_widget = create_callback_login_widget(bot_name, size=SMALL)

    context = {
        # 'telegram_login_widget': telegram_login_widget
    }

    return render(request, 'blog/sign_up.html', context )

