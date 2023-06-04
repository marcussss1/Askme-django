from django import template
from askme.models import Like, Question, Comment

register = template.Library()


@register.simple_tag
def check_likes(request_user, id, type):
    likes = Like.objects.like_sort(request_user, id, type)
    if likes.exists():
        return 'disabled="disabled"'
    else:
        return


@register.simple_tag
def check_dislikes(request_user, id, type):
    dislikes = Like.objects.dislike_sort(request_user, id, type)
    if dislikes.exists():
        return 'disabled="disabled"'
    else:
        return
