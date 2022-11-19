from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from datetime import datetime
from django.urls import reverse
from PIL import Image

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
    
    # добавить выбоор между первым и вторым корпусом
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

    slug = models.SlugField(max_length=50) # unique=True

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        print("PK", self.pk)
        return reverse('post_detail', kwargs={"pk": self.pk})

    def save(self):
        super().save()
        if self.image:
            print("Pruning")
            img = Image.open(self.image.path)

            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.image.path)