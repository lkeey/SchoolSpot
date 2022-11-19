from django import template

from blog.models import PostLike

register = template.Library()

@register.simple_tag
def was_liked(user, id):

    try:
        PostLike.objects.get(user=user, obj_id=id)
        return True
    except PostLike.DoesNotExist:
        return False