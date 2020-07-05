from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='liked_list')
def liked_list(model):
    return model.likes.all()

@register.filter(name='comment_liked_list')
def comment_liked_list(model):
    return model.cmt_likes.all()

@register.filter(name='saved_post')
def saved_post(profile):
    return [id for post, id, date in profile.saved_posts.values_list()]


@register.filter(name='user_in_follow_request')
def user_in_follow_request(current_user, follower):
    from users.models import FollowRequest
    if len(FollowRequest.objects.filter(from_user=current_user).filter(to_user=follower)) == 1:
        return True


@register.filter(name='get_nested_comment', needs_autoescape=True)    
def get_nested_comment(parent_id, root, autoescape=True):
    from django.utils import timesince
    from django_currentuser.middleware import (
        get_current_user, get_current_authenticated_user)
    from blog.models import Comment
    result_comment = ''
    rootId = root

    reply_comment = Comment.objects.filter(parent_comment_id=parent_id).order_by('id')
    if len(reply_comment)>0:
        for replied_to_comment in reply_comment:
            commented_date = timesince.timesince(replied_to_comment.comment_date)
            likeclass = ""
            commentflag = ""
            if get_current_authenticated_user() in replied_to_comment.cmt_likes.all():
                likeclass = "press"
            if replied_to_comment.flag:
                commentflag = "d-block"

            if get_current_authenticated_user().username == replied_to_comment.author.username:
    
                result_comment += '<li class="media" id="{3}">\
                    <a href="#"><img class="mr-3 profilePic" src="/media/default.jpeg" alt="img" width="50px" height="50px"></a>\
                    <div class="media-body">\
                        <h6 class="mt-0 mb-1 profileName">\
                        <a href="#">{0} {1}</a>\
                        <span class="ml-3 commentlikeBtn"><i class="fa fa-heart {8}" data-postid="{10}" data-catid="{3}" onclick="cmt_like(this)"></i></span>\
                        <span class="comment-editbtn d-block">\
                            <div class="dropleft">\
                                <p class="dropdown-toggle" data-toggle="dropdown"><i class="fa fa-ellipsis-v"></i></p>\
                                <div class="dropdown-menu">\
                                    <a class="dropdown-item" data-catid="{3}" onclick="editComment(event);">Edit</a>\
                                    <a class="dropdown-item deleteCommentbtn" data-catid="{3}" onclick="deleteCommentbtn(this)" data-toggle="modal" data-target="#deleteCommentModal">delete</a>\
                                </div>\
                            </div>\
                        </span>\
                        </h6>\
                        <div class="comment-main-content{3} mb-2">\
                            <p class="commentText">{2}</p>\
                            <div class="commentTextBottomBtn">\
                                <span class="textBtn">{7}</span>\
                                <span class="textBtn"><span class="likes_count{3}">{6}</span> likes</span>\
                                <span id="repltBtn{3}" class="textBtn nested-replyBtn" data-catid="{3}" data-parent_id="{4}" data-root="{5}" data-uname="{0} {1}" onclick="nestedReply(this);">reply</span>\
                                <span class="textBtn float-right text-edited text-theme {9}">edited</span>\
                            </div>\
                        </div>\
                        <div class="replace-maincontent{3}"></div>\
                    </div>\
                </li>'.format(replied_to_comment.author.first_name, replied_to_comment.author.last_name,
                              replied_to_comment.commented_text, replied_to_comment.id, parent_id, rootId,
                              replied_to_comment.cmt_likes_count, commented_date, likeclass, commentflag,
                              replied_to_comment.commented_post.id)
            else:
                result_comment += '<li class="media" >\
                    <a href="#"><img class="mr-3 profilePic" src="/media/default.jpeg" alt="img" width="50px" height="50px"></a>\
                    <div class="media-body">\
                        <h6 class="mt-0 mb-1 profileName">\
                        <a href="#">{0} {1}</a>\
                        <span class="ml-3 commentlikeBtn"><i class="fa fa-heart {8}" data-postid="{10}" data-catid="{3}" onclick="cmt_like(this)"></i></span>\
                        <span class="comment-editbtn">\
                            <div class="dropleft">\
                                <p class="dropdown-toggle" data-toggle="dropdown"><i class="fa fa-ellipsis-v"></i></p>\
                                <div class="dropdown-menu">\
                                    <a class="dropdown-item" data-catid="{3}" onclick="editComment(event);">Edit</a>\
                                    <a class="dropdown-item deleteCommentbtn" data-catid="{3}" onclick="deleteCommentbtn(this)" data-toggle="modal" data-target="#deleteCommentModal">delete</a>\
                                </div>\
                            </div>\
                        </span>\
                        </h6>\
                        <div class="comment-main-content{3} mb-2">\
                            <p class="commentText">{2}</p>\
                            <div class="commentTextBottomBtn">\
                                <span class="textBtn">{7}</span>\
                                <span class="textBtn"><span class="likes_count{3}">{6}</span> likes</span>\
                                <span id="repltBtn{3}" class="textBtn nested-replyBtn" data-catid="{3}" data-parent_id="{4}" data-root="{5}" data-uname="{0} {1}" onclick="nestedReply(this);">reply</span>\
                                <span class="textBtn float-right text-edited text-theme {9}">edited</span>\
                            </div>\
                        </div>\
                        <div class="replace-maincontent{3}"></div>\
                    </div>\
                </li>'.format(replied_to_comment.author.first_name, replied_to_comment.author.last_name,
                              replied_to_comment.commented_text, replied_to_comment.id, parent_id, rootId,
                              replied_to_comment.cmt_likes_count, commented_date, likeclass, commentflag,
                              replied_to_comment.commented_post.id)

            result_comment += get_nested_comment(replied_to_comment.id, rootId)

    return mark_safe(result_comment)


@register.filter(name='change_notification_status')
def change_notification_status(notification):
    notification.status = 'old'
    notification.save()
    return notification







