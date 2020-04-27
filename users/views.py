from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.views.generic.list import ListView
from blog.models import Post
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, View, TemplateView
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import CustomAuthForm
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test



def logout_required(function=None, logout_url=settings.LOGOUT_URL):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=logout_url
    )
    if function:
        return actual_decorator(function)

    return actual_decorator



def user_register(request):
    template = 'users/registrationForm.html'

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("Inside")

            if User.objects.filter(username=form.cleaned_data['username']).exists():
                return render(request, template, {'form': form,
                                                  'error_message': 'Username is not available'})
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                return render(request, template, {'form': form,
                                                  'error_message': 'Email already exists'})
            elif form.cleaned_data['password'] != form.cleaned_data['repeat_password']:
                return render(request, template, {'form': form,
                                                  'error_message': 'Passwords do not match'})
            else:
                user = User.objects.create_user(
                    form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                user.save()
                # messages.success(request, 'Registration successful, you can login now')
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
    template_name='users/login.html'
    authentication_form=CustomAuthForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("login-home")
        return self.render_to_response(self.get_context_data())



@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your profile has been updated successfully')
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    post = Post.objects.filter(author_id=request.user)
    article_category = [name for id, name in Profile.objects.get(user=request.user).article_category.values_list()]
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'article_category': article_category,
        'posts': post
    }

    return render(request, 'users/userprofile.html', context)


class HomeView(ListView):
    model = Post
    template_name = 'blog/loginhome.html'
    context_object_name = 'posts'
    ordering = ['date_posted']

    # def get_queryset(self):
    #     return Post.objects.all()


"""This is the view for other user's profile. URL path in  Blogging/urls"""


def other_user_profile(request, pk):
    post = Post.objects.filter(author_id=pk)
    user = User.objects.get(id=pk)
    context = {
        'posts': post,
        'user_id': user
    }

    print(post)

    return render(request, 'users/otherUserProfile.html', context)


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
        return redirect("profile")
