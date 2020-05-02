from .models import Post
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import NewPostForm
from django.contrib import messages
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from users.models import ArticleCategory

class HomeView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.all()[:5]


@login_required
def home(request):
    if request.method == 'POST':
        new_post_form = NewPostForm(request.POST)
        topicId = request.POST.getlist("topicId")

        if new_post_form.is_valid():
            new_post_form.instance.author = request.user
            new_post_form.save()
            messages.success(request, f'Your new post has been posted successfully')
            return redirect('login-home')
        
        if len(topicId):
            posts = Post.objects.filter(category__id__in = topicId).order_by('-date_posted')
            new_post_form = NewPostForm()
            topicId = [int(id) for id in topicId]
            context = {
                'new_post_form': new_post_form,
                'posts': posts,
                "topicId" : topicId,
                "category_list" : [(category.id, category.name) for category in ArticleCategory.objects.all()]
            }
            return render(request, 'blog/loginhome.html', context)
    
    else:
        new_post_form = NewPostForm()

    context = {}
    posts = Post.objects.all().order_by('-date_posted')
    context['new_post_form'] = new_post_form
    context['posts'] = posts
    context["category_list"] = [(category.id, category.name) for category in ArticleCategory.objects.all()]
    return render(request, 'blog/loginhome.html', context)


def post_update(request, pk):

    current_post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post_update_form = NewPostForm(request.POST, instance=current_post)

        if post_update_form.is_valid():
            post_update_form.save()
            messages.success(request,f'Your post has been updated successfully')
            return redirect('profile')

    else:
        post_update_form = NewPostForm()

    post = Post.objects.filter(author_id=request.user)

    context = {
        'post_update_form':post_update_form,
        'posts':post
    }

    return render(request,'users/userprofile.html',context)


class PostUpdateView(LoginRequiredMixin,UpdateView,UserPassesTestMixin):
    template_name = 'blog/update_post.html'
    model = Post
    fields = ['title','content','category']
    success_url = '/profile'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, DeleteView,UserPassesTestMixin):
    model = Post
    template_name = 'users/userprofile.html'
    success_url = '/profile'

    #messages.add_message(self.request,messages.SUCCESS,"Post deleted successfully")


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author








# class AboutView(DetailView):
#     template_name = "blog/about.html"

# def about(request):
#     context = {
#         'posts': posts
#     }
#     return render(request, 'blog/about.html', context)
