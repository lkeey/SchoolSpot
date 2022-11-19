from .models import Post
from django.forms import ModelForm, Textarea
 

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
