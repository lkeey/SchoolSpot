from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView, CreateView, 
    DetailView, View,
)
from datetime import datetime
from django.views.generic.edit import FormMixin
from django.urls.base import reverse_lazy
from django.http import HttpResponse
import json
from reportlab.pdfgen import canvas 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import PostCreateForm, GradeForm
from .models import (
        Student, Post,
        PostLike, Mark, Certificate
    )
from django.db.models import Count
from django.core import serializers
from django.core.paginator import Paginator
from django.http import JsonResponse

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
            'certificates': Certificate.objects.filter(student=student).order_by("-was_added")
        }

        return context

    def post(self, request, **kwargs):
        print("POST!!")
        student = Student.objects.get(user=request.user)

        if request.FILES.get('image') == None:
            image = student.profile_img
            
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')


        student.profile_img = image
        student.save()

        return redirect('student_profile')    

class PostDetailtView(DetailView):
    model = Post

    template_name = 'blog/post_detail.html'
    context_object_name = 'post_detail'

    def get_success_url(self, **kwargs):
       
        return reverse_lazy('post_detail', kwargs={"pk":self.get_object().id})
    
class LikekView(View):
    # в данную переменную будет устанавливаться модель закладок, которую необходимо обработать
    model = None

    def post(self, request, pk, id=0):
        user = auth.get_user(request)

        # проверка на существование лайка
        like, created = self.model.objects.get_or_create(user=user, obj_id=pk)

        print(f"USER {like.obj.author}\nCREATOR {user}\nOBJ_ID {pk}")

        print("MODEL-CLASS IS", like.obj)

        if not created:
            like.delete()

            like.obj.amount_of_likes -= 1
            like.obj.save()

        else:
            like.obj.amount_of_likes += 1
            like.obj.save()

        return HttpResponse(
            json.dumps({
                "result": created,
                "count": self.model.objects.filter(obj_id=pk).count()
            }),
            content_type="application/json"
        )    

class MarkView(View):
    model = Student

    def post(self, request):
        user = auth.get_user(request)

        print("USER", user, user.student.first().grade)

        Mark.objects.create(
            student=user.student.first()
        )

        print("Добавлена 5 -", user.student.first())

        return HttpResponse(
            json.dumps({
                "count": user.student.first().get_amount_marks(),
            }),
            content_type="application/json"
        )  

class CertificateView(View):
    model = Certificate

    def post(self, request, begin_date, end_date, student):
        user = auth.get_user(request)

        student = Student.objects.get(
            user__username=student
        )

        print("DATA - ", begin_date, end_date)

        Certificate.objects.get_or_create(
            student=student,
            date_begin=begin_date,
            date_end=end_date
        )

        print("Добавлен Сертификат -", student)

        return HttpResponse(
            json.dumps({
                "status": True,
            }),
            content_type="application/json"
        ) 


@login_required(login_url='sign_in')
def feed(request, page=0):
    # show all posts

    if request.method == "GET":

        context = {
            "page": page+1,
            "end_page": True if (Post.objects.all().count() >= (page+1)*5) else False, 
            "user": request.user,
            "student": request.user.student.first,
            "all_posts": Post.objects.all().order_by('-date_created')[5*page:5*(page+1)],
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

@login_required(login_url='sign_in')
def rating(request):
    form = GradeForm()

    if request.method == "POST":
        form = GradeForm(request.POST) 

        # begin_date = datetime.strptime(request.POST['begin_date']+"T00:00:00.000Z", '%Y-%m-%dT%H:%M:%S.%fZ').date() 
        # end_date = datetime.strptime(request.POST['end_date']+"T00:00:00.000Z", '%Y-%m-%dT%H:%M:%S.%fZ').date() 

        # print("DATE", request.POST['begin_date'])
        
        begin_date = str(request.POST['begin_date']) + "T00:00:00.000Z"
        end_date = str(request.POST['end_date']) + "T23:59:00.000Z"

        # 2021-10-22T16:00:00.000Z
        # %Y-%m-%dT%H:%M:%S.%fZ

        if form.is_valid(): 
            grade_form = form.cleaned_data['grade'] 
            obj = Student.objects.filter(grade=grade_form, owner__date_created__range=(begin_date, end_date))
            
            context = {
                "status": True,
                "form": form,
                "grade": grade_form,

                "begin_date": datetime.strptime(request.POST['begin_date'], '%Y-%m-%d').date() ,
                "end_date": datetime.strptime(request.POST['end_date'], '%Y-%m-%d').date() ,
                
                "begin_date_model": begin_date,
                "end_date_model": end_date,
                
                "results": obj,
                "prod": obj.annotate(count=Count('owner__id')).order_by('-count')[:5],
            }
            # https://django.fun/ru/qa/99584/
            
            return render(request, "blog/rating.html", context)
 
    context = {
        "status": False,
        "form": form,
    }

    return render(request, "blog/rating.html", context)

def show_pdf(request, begin_date, end_date):
    user = request.user
    student = Student.objects.get(user=user)

    response = HttpResponse(content_type='application/pdf') 
    response['Content-Disposition'] = f'attachment; filename="{student}.pdf"' 
    
    p = canvas.Canvas(response) 
    p.setFont("Times-Roman", 55) 
    p.drawString(100,700, f"{student} - ") 
    p.drawString(200,600, f"Является победителем среди учеников {student.grade} в акции '...'") 
    p.drawString(300,500, f"От {begin_date} До {end_date}") 
    p.showPage() 
    p.save() 
    
    return response 

def top_posts(request, page=0):
        # show all posts

    context = {
        "user": request.user,
        "page": page+1, 
        "end_page": True if (Post.objects.all().count() >= (page+1)*5) else False, 
        "student": request.user.student.first,
        "all_posts": Post.objects.annotate(count=Count("author_obj__id")).order_by('-count')[page*5:5*(page+1)],
    }

    return render(request, 'blog/posts_feed.html', context=context)


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
            return redirect('posts_feed', page=0)

        else:
            messages.warning(request, 'Data is invalid')

        
    # telegram_login_widget = create_callback_login_widget(bot_name, size=SMALL)

    context = {
        # 'telegram_login_widget': telegram_login_widget
    }

    return render(request, "blog/sign_in.html", context)

def loadMore(request):
    # next page
    print("LOOOOAD")

    if request.method == "POST":
        offset = int(request.POST['offset'])
        limit = 2
        posts = Post.objects.all().order_by('-date_created')[offset:offset+limit]
        totalData = Post.objects.count()
        posts_json = serializers.serialize("json", posts)
        print("posts_json", posts_json)
        return JsonResponse(
            data={
                "posts": posts_json,
                "totalResult": totalData,
            }
        )

def sign_up(request):
    # registration

    if request.method == 'POST':
        form = GradeForm(request.POST, request.FILES)

        if form.is_valid():
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
                        
                        new_profile = form.save(commit=False)
                        new_profile.user = user_model
                        new_profile.id_user = user_model.id
                        # new_profile = Student.objects.create(
                        #     user=user_model, 
                        #     id_user=user_model.id,
                        # )

                        new_profile.save()

                        messages.info(request, f'Hello, {user.username}')
                        messages.success(request, 'We are glad to see you in SchoolSpot')

                        data = {
                                # "all_posts": Post.objects.order_by('-date_created'),
                            }

                        # return render(request, 'discussions/posts_feed.html', data)
                        return redirect('posts_feed', page=0)
                else:
                    messages.info(request, 'The username must be more than 2 characters and the password more than 7')

            else:
                messages.info(request, 'Password is not matching')
                return redirect('sign_up')
        else:
            messages.warning(request, 'Data is invalid')


    # telegram_login_widget = create_callback_login_widget(bot_name, size=SMALL)

    context = {
        # 'telegram_login_widget': telegram_login_widget
        "formset": GradeForm

    }

    return render(request, 'blog/sign_up.html', context )

