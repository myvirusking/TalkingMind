from .models import Post
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render,HttpResponse
from django.urls import reverse_lazy
from .forms import NewPostForm
from django.contrib import messages
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from users.models import ArticleCategory
import json
from django.template.loader import render_to_string
from django.http import JsonResponse


class HomeView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all()[:5]


@login_required
def home(request):
    if request.method == 'POST':
        topicId = request.POST.getlist("topicId")


        if len(topicId):
            posts = Post.objects.filter(category__id__in = topicId).order_by('-date_posted')
            new_post_form = NewPostForm()
            topicId = [int(id) for id in topicId]
            context = {
                'posts': posts,
                "topicId" : topicId,
                "category_list" : [(category.id, category.name) for category in ArticleCategory.objects.all()]
            }
            return render(request, 'blog/loginhome.html', context)

    context = {}
    posts = Post.objects.all().order_by('-date_posted')
    context['posts'] = posts
    context["category_list"] = [(category.id, category.name) for category in ArticleCategory.objects.all()]
    return render(request, 'blog/loginhome.html', context)


def post_update(request, pk):
    current_post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post_update_form = NewPostForm(request.POST, instance=current_post)

        if post_update_form.is_valid():
            post_update_form.save()
            messages.success(request, f'Your post has been updated successfully')
            return redirect('profile')

    else:
        post_update_form = NewPostForm()

    post = Post.objects.filter(author_id=request.user)

    context = {
        'post_update_form': post_update_form,
        'posts': post
    }

    return render(request, 'users/userprofile.html', context)


class PostUpdateView(LoginRequiredMixin, UpdateView, UserPassesTestMixin):
    template_name = 'blog/update_post.html'
    model = Post
    # fields = ['title','content','category','image']
    success_url = '/profile'
    form_class = NewPostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            image = self.request.FILES["image"]
            self.object.image.delete(save=True)
        except Exception as e:
            pass
        return super().post(request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, DeleteView, UserPassesTestMixin):
    model = Post
    template_name = 'users/userprofile.html'
    success_url = '/profile'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy("login-home")
    form_class = NewPostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'Your new post has been posted successfully')
        return super().form_valid(form)


"""This view gets called as the user clicks on the like button. It get called through 
ajax (javascript/post_like.js) the url is in the Blogging/urls with the name 'like-post' 
State of the button is saved each time the user clicks that. Like button appearance changes
 depending on the liked button status"""

@login_required
def post_like(request):
    liked_button_status = 'liked'
    if request.method == 'GET':
        post_id = request.GET['post_id']
        liked_post = Post.objects.filter(id=post_id).first()
        users_who_liked_post = [user for id, user in liked_post.likes.values_list()]
        liked_button_status = 'none'
        if request.user.id in users_who_liked_post:
            liked_post.likes.all()[users_who_liked_post.index(request.user.id)].delete()
            user_count = liked_post.likes.all().count()
            print(user_count)
            data_dict = {'likes': user_count}
            return JsonResponse(data=data_dict, safe=False)

        else:
            liked_post.likes.create(user=request.user)
            user_count = liked_post.likes.all().count()
            print(user_count)
            data_dict = {'likes': user_count}
            return JsonResponse(data=data_dict, safe=False)

        return render(request, 'blog/loginhome.html', {'liked_button_status':liked_button_status})

    return render(request, 'blog/loginhome.html',{'liked_button_status':liked_button_status})



# class AboutView(DetailView):
#     template_name = "blog/about.html"

# def about(request):
#     context = {
#         'posts': posts
#     }
#     return render(request, 'blog/about.html', context)
