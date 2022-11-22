from django import template

from blog.models import PostLike, Certificate

register = template.Library()

@register.simple_tag
def was_liked(user, id):
    try:
        PostLike.objects.get(user=user, obj_id=id)
        return True
    except PostLike.DoesNotExist:
        return False

@register.simple_tag
def was_certificated(student, begin_date, end_date):
    try:
        Certificate.objects.get(
            student=student, 
            date_begin=begin_date,
            date_end=end_date,
            )

        return True
    except Certificate.DoesNotExist:
        
        return False

    