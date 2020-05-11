from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm, AboutForm
from django.contrib import messages
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import CustomAuthForm
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from blog.models import Post
from django.template.loader import render_to_string
from django.http import JsonResponse


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
                username =   form.cleaned_data['username'],
                email =   form.cleaned_data['email'],
                password =  form.cleaned_data['password']
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

    post = Post.objects.filter(author_id=request.user).order_by('-date_posted')
    article_category = [name for id, name in Profile.objects.get(user=request.user).article_category.values_list()]
    current_user_profile = Profile.objects.filter(user=request.user).first()

    following_count = current_user_profile.following_count
    followers_count = current_user_profile.followers_count

    following_users = [user for id, user in request.user.profile.following.values_list()]

    following_list = current_user_profile.following.all()
    followers_list = current_user_profile.followers.all()


    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'about_form':about_form,
        'article_category': article_category,
        'posts': post,
        'rec_request': rec_request,
        'following_count': following_count,
        'followers_count': followers_count,
        'following_list': following_list,
        'followers_list': followers_list,
        'following_users': following_users,

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
    if (request.user.id == pk):
        return HttpResponseRedirect('/profile')

    post = Post.objects.filter(author_id=pk)
    user = User.objects.get(id=pk)

    profile_other = Profile.objects.filter(id=pk).first()
    profile_current = Profile.objects.filter(id=request.user.id).first()

    following_list = profile_current.following.all()

    following_list_of_other_user = profile_other.following.all()
    follower_list_of_other_user = profile_other.following.all()

    button_status = 'none'

    if user.id not in [user for id, user in profile_current.following.values_list()]:

        button_status = 'not_following'

        if len(FollowRequest.objects.filter(from_user=request.user).
                       filter(to_user=user)) == 1:
            button_status = 'requested'

    other_user_article_category = [name for id, name in Profile.objects.get(user=user).article_category.values_list()]
    current_user_article_category = [name for id, name in Profile.objects.get(user=request.user).article_category.values_list()]
    common_topics = [name for name in current_user_article_category if name in other_user_article_category]

    following_count = profile_other.following_count
    follower_count = profile_other.followers_count

    context = {
        'posts': post,
        'user_id': user,
        'article_category': other_user_article_category,
        'button_status': button_status,
        'following_count': following_count,
        'follower_count': follower_count,
        'common_topics':common_topics,
        'following_list': following_list_of_other_user,
        'follower_list': follower_list_of_other_user
    }

    return render(request, 'users/otherUserProfile.html', context)


"""  This function gets called when the user follows some other user. Url path in Blogging/urls and the
 name of the url is "send_follow_request"   """


@login_required
def send_follow_request(request, pk):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=pk)
        frequest, created = FollowRequest.objects.get_or_create(
            from_user=request.user,
            to_user=user
        )

        return HttpResponseRedirect('/other-profile/{}/'.format(pk))


"""  This function gets called when the user cancels the follow request sent to  some other user. 
This wil  only be accessible after sending the follow request and before the acceptance of the request.
Url path in Blogging/urls and the name of the url is "cancel_follow_request"   """


@login_required
def cancel_follow_request(request, pk):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=pk)
        frequest = FollowRequest.objects.filter(
            from_user=request.user,
            to_user=user
        ).first()
        frequest.delete()
        return HttpResponseRedirect('/other-profile/{}/'.format(pk))


"""This view is called when the user who received the follow request deletes the request and this view 
is only accessible if the user receives any request. The Url path in Blogging/urls and the name of the 
url is "delete_follow_request" """


@login_required
def delete_follow_request(request, pk):
    from_user = get_object_or_404(User, id=pk)
    frequest = FollowRequest.objects.filter(
        from_user=from_user,
        to_user=request.user
    ).first()
    frequest.delete()
    return HttpResponseRedirect('/other-profile/{}/'.format(pk))


"""This view is called when the user who follows some other user, unfollows that user. This is accessible
only if the user follows that particular user. If this view is called then the user being unfollowed will 
 be removed from the following list of the user performing the action and also the user who is perfroming
  the unfollowing action will be removed from the followers list of the user being unfollowed. The Url 
  for the view is in Blogging/urls and the name of the url is "unfollow_user" """


@login_required
def unfollow_user(request, pk):
    user = get_object_or_404(User, id=pk)

    unfollowed_user = Profile.objects.get(id=pk)
    follower_list = [user for id, user in unfollowed_user.followers.values_list()]
    follower_user_index = follower_list.index(request.user.id)
    unfollowed_user.followers.all()[follower_user_index].delete()
    unfollowed_user.followers_count -= 1
    unfollowed_user.save()

    follower = Profile.objects.get(user=request.user)
    following_list = [user for id, user in follower.following.values_list()]
    following_user_index = following_list.index(pk)
    follower.following.all()[following_user_index].delete()
    follower.following_count -= 1
    follower.save()
    return HttpResponseRedirect('/other-profile/{}/'.format(pk))


"""This view gets called if the user who received the follow request accepts it. This is accessible 
only if the user receives any follow request. If this view gets called then the user who sent the follow 
request will be added in the followers list of the user who received the request and also the user 
who accepted the request will be added to the following list of the user who sent the request."""


@login_required
def accept_follow_request(request, pk):
    from_user = get_object_or_404(User, id=pk)

    frequest = FollowRequest.objects.filter(
        from_user=from_user, to_user=request.user).first()

    request_sender = from_user
    requested_user = frequest.to_user

    request_sender.profile.following.create(user=requested_user)
    request_sender.profile.following_count += 1
    request_sender.profile.save()

    requested_user.profile.followers.create(user=request_sender)
    requested_user.profile.followers_count += 1
    requested_user.profile.save()

    frequest.delete()

    return HttpResponseRedirect('/profile')


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
@login_required
def user_search_view(request):
    ctx = {}
    url_parameter = request.GET.get("q")

    users= []
    if url_parameter:
        users = User.objects.filter(username__icontains=url_parameter)
    

    ctx["users"] = users
    if request.is_ajax():
        print("Ajax request")

        html = render_to_string(
            template_name="blog/user-search-results.html", context={"users": users}
        )
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)

    return render(request, "blog/base.html", context=ctx)





