from django.contrib import admin
from .models import(
    Student,
    Post,
)

# Register your models here.
@admin.register(Post)
class PageAdmin(admin.ModelAdmin):
    list_display = ['slug', 'date_created']
    
    # автозаполнение
    prepopulated_fields = {
        "slug": ('content',),
    }


admin.site.register(Student)
