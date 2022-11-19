from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from datetime import datetime
from django.urls import reverse
from PIL import Image
import random
import string

# Create your models here.
User = get_user_model()

class Student(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='student',
    )

    id_user = models.IntegerField()
    
    bio = models.TextField(blank=True)
    
    telegram_id = models.IntegerField(default=0)

    profile_img = models.ImageField(
        upload_to='profile_images', 
        default='profile_images/blank-profile-img.png'
        )
    
    # добавить выбор между первым и вторым корпусом
    # добавить классы(Class, Teacher)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    author = models.ForeignKey(User,
                on_delete=models.CASCADE,
    )

    image = models.ImageField(upload_to='post_images')

    content = RichTextField('', blank=True, null=True,
                    max_length=5000,   
            )

    date_created = models.DateTimeField(default=datetime.now)

    date_updated = models.DateTimeField(auto_now=True)

    amount_of_likes = models.IntegerField(default=0)

    slug = models.SlugField(max_length=50, unique=True, blank = True) 

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        print("PK", self.pk)
        return reverse('post_detail', kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(4)

        super(Post, self).save(**kwargs)

        if self.image:
            print("Pruning")
            img = Image.open(self.image.path)

            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.image.path)

# LIKES
      
class LikesBase(models.Model):
    class Meta:
        abstract = True
 
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,    
    )
 
    def __str__(self):
        return self.user.username

class PostLike(LikesBase):
    class Meta:
        db_table = "like_post"

    obj = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )

def unique_slugify(length):

    # choose from all lowercase letter
    letters = string.ascii_lowercase

    result_str = ''.join(random.choice(letters))
    while True:
        
        for i in range(length):
            
            result_str += ''.join(random.choice(string.ascii_lowercase))
            result_str += ''.join(random.choice(string.punctuation))
            result_str += ''.join(random.choice(string.digits))
            
        if(not Post.objects.filter(slug=result_str).exists()):
            break  

    return result_str