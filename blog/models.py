from django.db import models
from django.contrib.auth import get_user_model

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

