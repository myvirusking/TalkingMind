from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.views.generic.list import ListView
from blog.models import Post
from django.contrib.auth.decorators import login_required
from blog import urls
from django.views.generic.edit import FormView
from django.views.generic import  CreateView


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
                messages.success(request, 'Registration successful, you can login now')

                return redirect('login')

        else:
            print(form.errors)

    else:
        form = RegisterForm()

    return render(request, template, {'form': form})


@login_required
def profile(request):

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES,instance = request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,f'Your profile has been updated successfully')
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance = request.user.profile)

    post = Post.objects.filter(author_id=request.user)
    context = {
        'user_form':user_form,
        'profile_form':profile_form,
        'posts':post
    }

    print(post)
    return render(request, 'users/userprofile.html',context)


class HomeView(ListView):
    model = Post
    template_name = 'blog/loginhome.html'
    context_object_name = 'posts'
    ordering = ['date_posted']

    # def get_queryset(self):
    #     return Post.objects.all()
