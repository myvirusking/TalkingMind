from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import Http404
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm, AboutForm
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import CustomAuthForm
from blog.forms import NewPostForm, CommentForm
from blog.forms import NewPostForm, CommentForm
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from blog.models import Post
from django.template.loader import render_to_string
from django.http import JsonResponse
from settings.models import AccountPrivacySetting
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import Blogging.settings
from django.contrib.auth import signals
from django.http import HttpResponseRedirect




#global variable for making efficient infinite scrolling
global_posts = None
global_profile_post_paginator = None
global_otherprofile_post_paginator = None


#################  Currently not in use but could be used in future development##################
def logout_required(function=None, logout_url=settings.LOGOUT_URL):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=logout_url
    )
    if function:
        return actual_decorator(function)

    return actual_decorator


###################################################################################################


def user_register(request):
    template = 'users/registrationForm.html'

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {'form': form,
                                                  'error_message': 'Username is already taken '})
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {'form': form,
                                                  'error_message': 'Email already exists'})
            elif form.cleaned_data['password'] != form.cleaned_data['repeat_password']:
                return render(request, template, {'form': form,
                                                  'error_message': 'Passwords do not match'})
            else:
                user = User.objects.create_user(

                    first_name = form.cleaned_data['first_name'],
                    last_name =  form.cleaned_data['last_name'],
                    username = form.cleaned_data['username'],
                    email = form.cleaned_data['email'],
                    password = form.cleaned_data['password']

                )
                user.save()
                user = authenticate(request, username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'])
                login(request, user)
                return redirect('fav_article_category')

        else:
            print(form.errors)

    else:
        form = RegisterForm()

    return render(request, template, {'form': form})



class CustomLoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomAuthForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("login-home")
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


@login_required
def profile(request):
    rec_request = FollowRequest.objects.filter(to_user=request.user.id)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        about_form = AboutForm(request.POST, instance = request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
        else:
            print("Invalid")

        if about_form.is_valid():
            about_form.save()
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        about_form = AboutForm(instance=request.user.profile)

    article_category = [name for id, name in Profile.objects.get(user=request.user).article_category.values_list()]
    current_user_profile = Profile.objects.filter(user=request.user).first()

    following_count = current_user_profile.following_count
    followers_count = current_user_profile.followers_count

    following_users = [user for id, user in request.user.profile.following.values_list()]
    following_list = current_user_profile.following.all().order_by("user")
    followers_list = current_user_profile.followers.all().order_by("user")

    comment_form = CommentForm(auto_id=False)

    #infinite scrolling with the help of pagination
    page = request.GET.get('page', 1)
    if int(page) == 1:
        global global_posts,global_profile_post_paginator
        global_posts = Post.objects.filter(author_id=request.user).order_by('-date_posted')
        global_profile_post_paginator = Paginator(global_posts, settings.POST_PAGINATION_PER_PAGE)
    try:
        paginated_posts = global_profile_post_paginator.page(page)
    except PageNotAnInteger:
        paginated_posts = global_profile_post_paginator.page(1)
    except EmptyPage:
        paginated_posts = global_profile_post_paginator.page(global_profile_post_paginator.num_pages)
    print(global_posts.count())
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'about_form':about_form,
        'article_category': article_category,
        'paginated_posts': paginated_posts,
        'posts_count' : global_posts.count(),
        'rec_request': rec_request,
        'following_count': following_count,
        'followers_count': followers_count,
        'following_list': following_list,
        'followers_list': followers_list,
        'following_users': following_users,
        'comment_form': comment_form,

    }

    return render(request, 'users/userprofile.html', context)


class HomeView(ListView):
    model = Post
    template_name = 'blog/loginhome.html'
    context_object_name = 'posts'
    ordering = ['date_posted']


"""This is the view for other user's profile. URL path in  Blogging/urls"""


@login_required
def other_user_profile(request, pk):

    if request.user.id == pk:
        return HttpResponseRedirect('/profile')

    user = User.objects.get(id=pk)

    if request.user in user.profile.blocked_users.all():
        print("User not found   ")
        raise Http404("User doesn't exist")

    if user not in request.user.profile.blocked_users.all():


        #infinite scrolling with the help of pagination
        page = request.GET.get('page', 1)
        if int(page) == 1:
            global global_posts,global_otherprofile_post_paginator
            global_posts = Post.objects.filter(author_id=pk).order_by('-date_posted')
            global_otherprofile_post_paginator = Paginator(global_posts, settings.POST_PAGINATION_PER_PAGE)
        try:
            paginated_posts = global_otherprofile_post_paginator.page(page)
        except PageNotAnInteger:
            paginated_posts = global_otherprofile_post_paginator.page(1)
        except EmptyPage:
            paginated_posts = global_otherprofile_post_paginator.page(global_otherprofile_post_paginator.num_pages)

        user = User.objects.get(id=pk)

        profile_other = Profile.objects.filter(id=pk).first()
        profile_current = Profile.objects.filter(user=request.user).first()

        following_list = profile_current.following.all()

        profile_privacy_setting = AccountPrivacySetting.objects.get(user=user)
        profile_privacy = profile_privacy_setting.profile_privacy

        following_list_of_other_user = profile_other.following.all()
        follower_list_of_other_user = profile_other.followers.all()

        button_status = 'none'
        button_class = 'unfollowBtn'
        button_id = 'unfollow-user'
        button_text = 'Unfollow'

        if user.id not in [user for id, user in profile_current.following.values_list()]:

            button_status = 'not_following'
            button_class = 'followBtn'
            button_id = 'follow-user'
            button_text = 'Follow'
            user_follows_profile = False

            if len(FollowRequest.objects.filter(from_user=request.user).filter(to_user=user)) == 1:
                button_status = 'requested'
                button_class = 'cancelRequestBtn'
                button_id = 'cancel-request'
                button_text = 'Cancel request'
        else:
            user_follows_profile = True
        other_user_article_category = [name for id, name in Profile.objects.get(user=user).article_category.values_list()]
        current_user_article_category = [name for id, name in Profile.objects.get(user=request.user).article_category.values_list()]
        common_topics = [name for name in current_user_article_category if name in other_user_article_category]
        current_user_following_list = [user for id, user in request.user.profile.following.values_list()]

        following_count = profile_other.following_count
        follower_count = profile_other.followers_count

        comment_form = CommentForm(auto_id=False)

        context = {
            'paginated_posts': paginated_posts,
            'posts_count' : global_posts.count(),
            'user_id': user,
            'article_category': other_user_article_category,
            'button_status': button_status,
            'button_class':button_class,
            'button_id' : button_id,
            'button_text':button_text,
            'following_count': following_count,
            'follower_count': follower_count,
            'common_topics':common_topics,
            'following_list': following_list_of_other_user,
            'follower_list': follower_list_of_other_user,
            'following_list_of_current_user': current_user_following_list,
            'comment_form': comment_form,
            'profile_privacy':profile_privacy,
            'user_follows_profile':user_follows_profile,
            'block_user_class':'block',
            'block_user_text': 'Block user'
        }

    else:
        profile_privacy_setting = AccountPrivacySetting.objects.get(user=user)
        profile_privacy = profile_privacy_setting.profile_privacy
        context = {
            'paginated_posts': [],
            'posts_count': 0,
            'user_id': user,
            'article_category': [],
            'button_status': "blocked",
            'button_class': "unblock",
            'button_id': "unblock-user",
            'button_text': "Unblock",
            'following_count': 0,
            'follower_count': 0,
            'common_topics': [],
            'following_list': [],
            'follower_list': [],
            'following_list_of_current_user': [],
            'profile_privacy': profile_privacy,
            'user_follows_profile': False,
            'block_user_class': 'unblock',
            'block_user_text': 'Unblock user'


        }
    return render(request, 'users/otherUserProfile.html', context)


"""  This function gets called when the user follows some other user. Url path in Blogging/urls and the
     name of the url is "send_follow_request.js"   """


@login_required
def send_follow_request(request):
    if request.user.is_authenticated:
        userid = request.GET['userid']
        user = get_object_or_404(User, id=userid)

        accout_setting = AccountPrivacySetting.objects.get(user=user)
        profile_privacy_of_other_user = accout_setting.profile_privacy

        if profile_privacy_of_other_user == 'public':
            print("Inside")
            request.user.profile.following.create(user=user)
            request.user.profile.following_count += 1
            request.user.profile.save()

            user.profile.followers.create(user=request.user)
            user.profile.followers_count += 1
            user.profile.notification.create(from_user=request.user,
                                             notification_title= "started following you",
                                             notification_content="",
                                             notification_type="followed_by")
            user.profile.notification_count += 1

            user.profile.save()

            following_count = request.user.profile.following_count

            data_dict = {'profile_privacy': 'public',
                         'following_count': following_count}
            return JsonResponse(data=data_dict, safe=False)

        elif profile_privacy_of_other_user == 'private':
            frequest, created = FollowRequest.objects.get_or_create(
                from_user=request.user,
                to_user=user
            )
            user.profile.notification.create(from_user=request.user,
                                             notification_title="Follow request from ",
                                             notification_content="",
                                             notification_type="follow_request")
            user.profile.notification_count += 1
            user.profile.save()

            data_dict = {'profile_privacy': 'private'}

            return JsonResponse(data=data_dict, safe=False)


        return render(request, 'users/userprofile.html')

"""  This function gets called when the user cancels the follow request sent to  some other user. 
This wil  only be accessible after sending the follow request and before the acceptance of the request.
Url path in Blogging/urls and the name of the url is "cancel_follow_request"   """


@login_required
def cancel_follow_request(request):
    if request.user.is_authenticated:
        userid = request.GET['userid']
        user = get_object_or_404(User, id=userid)
        frequest = FollowRequest.objects.filter(
            from_user=request.user,
            to_user=user
        ).first()
        frequest.delete()

        try:
            user.profile.notification.get(from_user=request.user,notification_type="follow_request").delete()
            user.profile.notification_count -=1
        except:
            pass

    return render(request, 'users/userprofile.html')


"""This view is called when the user who received the follow request deletes the request and this view 
is only accessible if the user receives any request. The Url path in Blogging/urls and the name of the 
url is "delete_follow_request" """


@login_required
def delete_follow_request(request):
    if request.user.is_authenticated:
        userid = request.GET['userid']
        from_user = get_object_or_404(User, id=int(userid))
        frequest = FollowRequest.objects.filter(
            from_user=from_user,
            to_user=request.user
        ).first()
        frequest.delete()
        return render(request, 'users/notifications.html')


"""This view is called when the user who follows some other user, unfollows that user. This is accessible
only if the user follows that particular user. If this view is called then the user being unfollowed will 
 be removed from the following list of the user performing the action and also the user who is perfroming
  the unfollowing action will be removed from the followers list of the user being unfollowed. The Url 
  for the view is in Blogging/urls and the name of the url is "unfollow_user" """


@login_required
def unfollow_user(request):
    if request.user.is_authenticated:
        userid = request.GET['userid']
        user = get_object_or_404(User, id=int(userid))

        unfollowed_user = Profile.objects.get(id=int(userid))
        follower_list = [user for id, user in unfollowed_user.followers.values_list()]
        follower_user_index = follower_list.index(request.user.id)
        unfollowed_user.followers.all()[follower_user_index].delete()
        unfollowed_user.followers_count -= 1

        try:
            user.profile.notification.get(from_user=request.user, notification_type="followed_by").delete()
            user.profile.notification_count -=1
        except:
            pass

        unfollowed_user.save()

        follower = Profile.objects.get(user=request.user)
        following_list = [user for id, user in follower.following.values_list()]
        following_user_index = following_list.index(int(userid))
        follower.following.all()[following_user_index].delete()
        follower.following_count -= 1
        follower.save()

        following_count = follower.following_count

        data_dict = {'following_count':following_count}

        return JsonResponse(data=data_dict, safe=False)

    return render(request, 'users/userprofile.html')



"""This view gets called if the user who received the follow request accepts it. This is accessible 
only if the user receives any follow request. If this view gets called then the user who sent the follow 
request will be added in the followers list of the user who received the request and also the user 
who accepted the request will be added to the following list of the user who sent the request."""


@login_required
def accept_follow_request(request):
    if request.user.is_authenticated:
        userid = request.GET['userid']
        from_usr = get_object_or_404(User, id=int(userid))

        frequest = FollowRequest.objects.filter(
            from_user=from_usr, to_user=request.user).first()

        request_sender = from_usr
        requested_user = request.user

        request_sender.profile.following.create(user=requested_user)
        request_sender.profile.following_count += 1
        request_sender.profile.save(update_fields=["following_count"])

        requested_user.profile.followers.create(user=request_sender)
        requested_user.profile.followers_count += 1
        requested_user.profile.save(update_fields=["followers_count"])

        request_sender.profile.notification.create(from_user=request.user,
                                             notification_title=" Approved your request",
                                             notification_content="",
                                             notification_type="follow_request_approved")
        request_sender.profile.notification_count += 1
        request_sender.profile.save(update_fields=["notification_count"]) 

        print(request_sender)

        try:
            requested_user.profile.notification.get(from_user=request_sender, notification_type="follow_request").delete()
            request.user.profile.notification_count -=1
            request.user.profile.save(update_fields=["notification_count"])
            print("In try")
        except Exception as e:
            print(e)


        frequest.delete()

    return render(request, 'users/notifications.html')


@login_required
def remove_from_followers_list(request):
    if request.user.is_authenticated:
        userid = request.GET['userid']
        user_to_be_removed = get_object_or_404(User, id=int(userid))

        follower_list = [user for id, user in request.user.profile.followers.values_list()]
        user_to_be_removed_index = follower_list.index(user_to_be_removed.id)
        request.user.profile.followers.all()[user_to_be_removed_index].delete()
        request.user.profile.followers_count -= 1
        request.user.profile.save()

        following_list_of_user_to_be_removed = [user for id, user in user_to_be_removed.profile.following.values_list()]
        removing_user_index = following_list_of_user_to_be_removed.index(request.user.id)
        user_to_be_removed.profile.following.all()[removing_user_index].delete()
        user_to_be_removed.profile.following_count -=1
        user_to_be_removed.profile.save()

        try:
            user_to_be_removed.profile.notification.get(from_user=request.user,
                                                    notification_type="follow_request_approved").delete()
            request.user.profile.notification_count -= 1
            print("In try")
        except Exception as e:
            print(e)

        removing_user_followers_count = request.user.profile.followers_count
        data_dict = {'followers_count':removing_user_followers_count}

        return JsonResponse(data=data_dict, safe=False)

    return render(request, 'users/userprofile.html')



class SelectFavouriteArticleCategoryView(LoginRequiredMixin, View):
    template_name = "users/select_fav_article_category.html"
    context = {}

    def get(self, *args, **kwargs):
        self.context["category_list"] = [(category.id, category.name) for category in ArticleCategory.objects.all()]
        self.context["category_selected_id_list"] = [id for id, name in Profile.objects.get(
            user=self.request.user).article_category.values_list()]
        return render(self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        slected_article_category_list = self.request.POST.getlist("check")
        slected_article_obj_list = []
        for id in slected_article_category_list:
            slected_article_obj_list.append(ArticleCategory.objects.get(id=id))
        user = self.request.user
        profile_obj = Profile.objects.get(user=user)
        profile_obj.article_category.set(slected_article_obj_list)
        profile_obj.save()
        return redirect("login-home")

# user search view
# @login_required
# def user_search_view(request):
#     ctx = {}
#     url_parameter = request.GET.get("q")
#
#     users= []
#     if url_parameter:
#         print(request.user.profile.blocked_by.all())
#         all_user = User.objects.filter(username__icontains=url_parameter)
#         blocked_by_list = request.user.profile.blocked_by.all()
#         qs3 = all_user.difference(blocked_by_list)
#         users = qs3
#
#     ctx["users"] = users
#     if request.is_ajax():
#         print("Ajax request")
#
#         html = render_to_string(
#             template_name="blog/user-search-results.html", context={"users": users}
#         )
#         data_dict = {"html_from_view": html}
#         return JsonResponse(data=data_dict, safe=False)
#
#     return render(request, "blog/base.html", context=ctx)


#user search view
@login_required
def user_search_view(request):
    ctx = {}
    url_parameter = request.GET.get("q")

    users= []
    if url_parameter:
        all_user = User.objects.filter(
            Q(username__icontains=url_parameter ) |
            Q(first_name__icontains=url_parameter) |
            Q(last_name__icontains=url_parameter)
            ).distinct()
        blocked_by_list = request.user.profile.blocked_by.all()
        qs3 = all_user.difference(blocked_by_list)
        users = qs3
    

    ctx["users"] = users
    if request.is_ajax():
        print("Ajax request")

        html = render_to_string(
            template_name="blog/user-search-results.html", context={"users": users,"searchVal":url_parameter}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(request, "blog/base.html", context=ctx)

#search by username
# @login_required
# def user_search_name(request):
#     ctx = {}
#     url_parameter = request.GET.get("q")

#     name= []
#     if url_parameter:
#         name = User.objects.filter(first_name__icontains=url_parameter)
    

#     ctx["name"] = name
#     if request.is_ajax():
#         print("Ajax name request")

#         html = render_to_string(
#             template_name="blog/user-search-results.html", context={"name": name}
#         )
#         data_dict = {"html_from_view": html}
#         return JsonResponse(data=data_dict, safe=False)

#     return render(request, "blog/base.html", context=ctx)

""" This view function is used for directing user to the search results page i.e user_list.html when the user search for some other users 
in the search-form field and if the results are found it will show the users profile fetch from the database and if the user is not found
it will simply show that no results with the search query is available
"""

@login_required
def user_search_list(request):
    ctx = {}
    # obj = User.objects.get(id=2)

    # ctx = {
    #     'name': obj.first_name,
    #     'username' :obj.username
    # }
    if 'name' in request.POST:
        url_parameter = request.POST['name']
    else:
        url_parameter = False
        
    
    if url_parameter:
        all_user = User.objects.filter(
            Q(first_name__startswith=url_parameter) |
            Q(last_name__startswith=url_parameter) |
            Q(username__startswith=url_parameter) 
            ).all()
        blocked_by_list = request.user.profile.blocked_by.all()
        qs3 = all_user.difference(blocked_by_list)
        users = qs3
        ctx = {
            'name': users,
            'search':url_parameter
        }
        
    return render(request, "blog/user_list.html", context=ctx)


@login_required
def notification_view(request):
    if request.user.is_authenticated:
        notification_list = request.user.profile.notification.all().order_by('-id')

        ctx = {'notification_list':notification_list} 

        return render(request,"users/notifications.html", context=ctx)


@login_required
def block_user(request):
    if request.method == 'GET':
        blocked_user_id = request.GET['userid']
        blocked_user_obj = User.objects.get(id=blocked_user_id)
        request.user.profile.blocked_users.add(blocked_user_obj)
        blocked_user_obj.profile.blocked_by.add(request.user)

        current_user_following = True
        blocked_user_following = True
        request_to = False
        request_from = False
        if blocked_user_obj.id not in [user for id, user in request.user.profile.following.values_list()]:

            current_user_following = False

        elif len(FollowRequest.objects.filter(from_user=request.user).filter(to_user=blocked_user_obj)) == 1:
            request_to = True

        if request.user.id not in [user for id, user in blocked_user_obj.profile.following.values_list()]:
            blocked_user_following = False

        elif len(FollowRequest.objects.filter(from_user=blocked_user_obj).filter(to_user=request.user)) == 1:
            request_from = True

        if current_user_following:
            follower_list = [user for id, user in blocked_user_obj.profile.followers.values_list()]
            follower_user_index = follower_list.index(request.user.id)
            blocked_user_obj.profile.followers.all()[follower_user_index].delete()
            blocked_user_obj.profile.followers_count -= 1

            try:
                blocked_user_obj.profile.notification.get(from_user=request.user, notification_type="followed_by").delete()
                blocked_user_obj.profile.notification_count -= 1
            except:
                pass

            blocked_user_obj.profile.save()

            following_list = [user for id, user in request.user.profile.following.values_list()]
            following_user_index = following_list.index(blocked_user_obj.id)
            request.user.profile.following.all()[following_user_index].delete()
            request.user.profile.following_count -= 1
            request.user.profile.save()

        elif request_to:
            frequest = FollowRequest.objects.filter(
                from_user=request.user,
                to_user=blocked_user_obj
            ).first()
            frequest.delete()

            try:
                blocked_user_obj.profile.notification.get(from_user=request.user, notification_type="follow_request").delete()
                blocked_user_obj.profile.notification_count -= 1
            except:
                pass

        if blocked_user_following:
            follower_list = [user for id, user in request.user.profile.followers.values_list()]
            follower_user_index = follower_list.index(blocked_user_obj.id)
            request.user.profile.followers.all()[follower_user_index].delete()
            request.user.profile.followers_count -= 1

            try:
                request.user.profile.notification.get(from_user=blocked_user_obj,
                                                          notification_type="followed_by").delete()
                blocked_user_obj.profile.notification_count -= 1
            except:
                pass

            request.user.profile.save()

            following_list = [user for id, user in blocked_user_obj.profile.following.values_list()]
            following_user_index = following_list.index(request.user.id)
            blocked_user_obj.profile.following.all()[following_user_index].delete()
            blocked_user_obj.profile.following_count -= 1
            blocked_user_obj.profile.save()

        elif request_from:
            frequest = FollowRequest.objects.filter(
                from_user=blocked_user_obj,
                to_user=request.user
            ).first()
            frequest.delete()

            try:
                blocked_user_obj.profile.notification.get(from_user=blocked_user_obj,
                                                          notification_type="follow_request").delete()
                blocked_user_obj.profile.notification_count -= 1
            except:
                pass

        return render(request, 'users/otherUserProfile.html')


@login_required
def unblock_user(request):
    if request.method == 'GET':
        unblocked_user_id = request.GET['userid']
        unblocked_user_obj = User.objects.get(id=unblocked_user_id)
        request.user.profile.blocked_users.remove(unblocked_user_obj)
        unblocked_user_obj.profile.blocked_by.remove(request.user)

    return render(request, 'users/otherUserProfile.html')












