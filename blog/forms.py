from .models import Post, Student, Mark
from django.forms import ModelForm, Textarea
from django.contrib.admin import widgets 
from django import forms
from datetime import datetime

class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.fields['content'].widget = Textarea(
            attrs= {
                'rows': 10,
                'class':'input-comment',
                'placeholder': 'Share Your Thoughts:',
            }
        )
        
        self.fields['content'].widget.attrs['class'] = 'form-control, input-post-content'

class GradeForm(ModelForm):
    class Meta:
        model = Student
        fields = ('grade',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['grade'].widget.attrs['class'] = 'btn dropdown-toggle dropdown-toggle-split grade-form'

