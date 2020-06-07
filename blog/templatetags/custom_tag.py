from django import template
register = template.Library()


@register.filter(name='liked_list')
def liked_list(model):
    return [user for id, user in model.likes.values_list()]


@register.filter(name='saved_post')
def saved_post(profile):
    return [id for post,id, date in profile.saved_posts.values_list()]


@register.filter(name='user_in_follow_request')
def user_in_follow_request(current_user, follower):
    from users.models import FollowRequest
    if len(FollowRequest.objects.filter(from_user=current_user).filter(to_user=follower)) == 1:
        return True


