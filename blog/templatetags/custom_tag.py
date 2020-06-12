from django import template
from django.utils.safestring import mark_safe
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


@register.filter(name='get_nested_comment', needs_autoescape=True)
def get_nested_comment(parent_id, root, autoescape=True):
    from blog.models import Comment
    result_comment = ''
    rootId = root
    reply_comment = Comment.objects.filter(parent_comment_id=parent_id).order_by('id')
    if len(reply_comment) > 0:
        for replied_to_comment in reply_comment:
            result_comment += '<li class="media" >\
                    <a href="#"><img class="mr-3 profilePic" src="/media/default.jpeg" alt="img" width="50px" height="50px"></a>\
                    <div class="media-body">\
                        <h6 class="mt-0 mb-1 profileName"><a href="#">{0} {1}</a><span class="ml-3 commentlikeBtn"><i class="fa fa-heart"></i></span></h6>\
                        <p class="commentText">{2}</p>\
                        <div class="commentTextBottomBtn">\
                            <span class="textBtn">0 minutes</span>\
                            <span class="textBtn"><span>0</span> likes</span>\
                            <span id="repltBtn{3}" class="textBtn nested-replyBtn" data-catid="{3}" data-parent_id="{4}" data-root="{5}" data-uname="{0} {1}" onclick="nestedReply(this);">reply</span>\
                        </div>\
                    </div><p>{4}</p>\
                </li>'.format(replied_to_comment.author.first_name, replied_to_comment.author.last_name,
                              replied_to_comment.commented_text, replied_to_comment.id, parent_id, rootId)
            print(parent_id)

            result_comment += get_nested_comment(replied_to_comment.id, rootId)

    return mark_safe(result_comment)


@register.filter(name='change_notification_status')
def change_notification_status(notification):
    notification.status = 'old'
    notification.save()
    return notification







