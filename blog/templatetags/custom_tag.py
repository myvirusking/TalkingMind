from django import template

register = template.Library()

@register.filter(name='liked_list')
def liked_list(model):
    return [user for id, user in model.likes.values_list()]


@register.filter(name='saved_post')
def saved_post(profile):
    return [id for post,id, date in profile.saved_posts.values_list()]
