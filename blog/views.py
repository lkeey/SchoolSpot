from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Student

# Create your views here.

@login_required(login_url='sign_in')
def feed(request):
    # show all posts
    return render(request, 'blog/posts_feed.html')

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

