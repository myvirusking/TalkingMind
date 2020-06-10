from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render,HttpResponse
from django.urls import reverse_lazy
from .forms import NewPostForm, CommentForm
from django.contrib import messages
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from users.models import ArticleCategory
from users.models import Profile, SavedPost
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from settings.models import AccountPrivacySetting
from django.db.models import Q

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

    list_of_following_users = [user for user in request.user.profile.following.values_list('user', flat=True)]
    list_of_public_account = AccountPrivacySetting.objects.filter(profile_privacy='public').values_list('user', flat=True)


    context = {}
    comment_form = CommentForm(auto_id=False)
    posts = Post.objects.filter(Q(author_id__in=list_of_following_users)|
                                Q(author_id__in=list_of_public_account)).order_by('-date_posted')
    context['posts'] = posts
    context['comment_form'] = comment_form
    context['home_page'] = 'active'
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
        imgSelectedList = self.request.FILES.getlist("images")
        postImgId = self.request.POST.getlist("postImgId")
        self.object = form.save()
        dbPostImgId = [str(postImage.id) for postImage in self.object.images.all()]
        deletedPostImgId = [imgId for imgId in dbPostImgId if imgId not in postImgId]
        if imgSelectedList:
            for imgSelected in imgSelectedList:
                postImgObj= PostImages.objects.create(user=self.request.user,image=imgSelected)
                self.object.images.add(postImgObj)
        if deletedPostImgId:
            for imgId in deletedPostImgId:
                postImgObj = PostImages.objects.get(id=int(imgId))
                postImgObj.image.delete()
                postImgObj.delete()

        return super().form_valid(form)

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
        imgSelectedList = self.request.FILES.getlist("images")
        self.object = form.save()
        if len(imgSelectedList)>0:
            postImgList = [PostImages.objects.create(user=self.request.user,image=imgSelected) for imgSelected in imgSelectedList]
            self.object.images.set(postImgList)
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


"""This view gets called as the user clicks on the like button. It gets called through 
ajax (javascript/post_like.js) the url is in the Blogging/urls with the name 'like-post' 
State of the button is saved each time the user clicks that. Like button appearance changes
 depending on the liked button status"""


@login_required
def post_like(request):
    if request.method == 'GET':
        post_id = request.GET['post_id']
        liked_post = Post.objects.get(id=int(post_id))
        users_who_liked_post = [user for id, user in liked_post.likes.values_list()]
        if request.user.id in users_who_liked_post:

            liked_post.likes.all()[users_who_liked_post.index(request.user.id)].delete()

            liked_post.likes_count -= 1

            liked_post.author.profile.notification.get(from_user=request.user,
                                                     notification_type="post_like",
                                                     post_involved=liked_post).delete()
            liked_post.author.profile.notification_count -= 1

        else:
            liked_post.likes.create(user=request.user)
            liked_post.likes_count +=1
            liked_post.author.profile.notification.create(from_user=request.user,
                                             notification_title="Liked your post",
                                             notification_content=liked_post.title,
                                             notification_type="post_like",
                                             post_involved=liked_post)
            liked_post.author.profile.notification_count += 1

        liked_post.save(update_fields=["likes_count"])
        likes_count = liked_post.likes_count
        data_dict = {'likes': likes_count}
        return JsonResponse(data=data_dict, safe=False)



"""This view gets called when the user clicks on save post button. It gets called through 
'javascript/post_save.js'. The url for the view is in 'Blogging/urls' and the name of the path is
 'save-post'. If the user saves the post then the color of button will turn to black and if the
  user again clicks on the button the post will be removed from his saved list.  Each time user saves
a post the save_count in the profile model will be incremented and if he remove the post from saved
list the counter will be decremented"""


@login_required
def save_post(request):
    if request.method == 'GET':
        post_id = request.GET['post_id']
        profile = Profile.objects.get_obj_or_404(user=request.user)
        saved_post = Post.objects.get_obj_or_404(id=post_id)
        saved_posts_list = [id for post, id, date in profile.saved_posts.values_list()]

        if saved_post.id in saved_posts_list:
            profile.saved_posts.all()[saved_posts_list.index(saved_post.id)].delete()
            profile.saved_posts_count -= 1

        else:
            profile.saved_posts.create(post=saved_post)
            profile.saved_posts_count += 1

        profile.save()

        save_count = profile.saved_posts_count
        data_dict = {'saves': save_count}
        return JsonResponse(data=data_dict, safe=False)


@login_required
def comment_like(request, pid):
    print('comment like')
    if request.method == 'GET':
        cmt_id = request.GET['cmt_id']
        liked_comment = Comment.objects.filter(id=int(cmt_id)).first()
        user_who_liked_cmt = [user for id, user in liked_comment.cmt_likes.values_list()]

        if request.user.id in user_who_liked_cmt:
            print("user in user_who_liked_cmt")
            print(liked_comment.cmt_likes.all()[user_who_liked_cmt.index(request.user.id)].delete())
            liked_comment.cmt_likes_count -= 1
            liked_comment.save()

            cmt_likes_count = liked_comment.cmt_likes_count
            data_dict = {'likes_count': cmt_likes_count}
            return JsonResponse(data=data_dict, safe=False)

        else:
            print("user not in user_who_liked_cmt")
            liked_comment.cmt_likes.create(user=request.user)
            liked_comment.cmt_likes_count += 1
            liked_comment.save()

            cmt_likes_count = liked_comment.cmt_likes_count
            data_dict = {'likes_count': cmt_likes_count}
            return JsonResponse(data=data_dict, safe=False)
    return render(request, 'blog/singlePost.html')


def single_post(request, pid):
    singlePost = Post.objects.filter(id=pid).first()
    comment_form = CommentForm()
    allComments = singlePost.comments.filter(parent_comment_id=0).order_by('-id')

    context = {
        'singlePost': singlePost,
        'comment_form': comment_form,
        'allComments': allComments,
    }

    return render(request, 'blog/singlePost.html', context)


@csrf_exempt
def comment(request):
    if request.method == 'POST':
        text = request.POST['commentText']
        postId = request.POST['postId']
        commentId = int(request.POST['commentId'])
        post = Post.objects.filter(id=postId).first()
        full_name = request.user.first_name + ' ' + request.user.last_name

        print(commentId)

        latest_comment = post.comments.create(commented_post=post, author=request.user, commented_text=text,
                                              parent_comment_id=commentId)

        print(latest_comment.commented_text)
        print(latest_comment.parent_comment_id)
        # print(Comment.objects.latest('id'))

        data_obj = {
            'commented_text': latest_comment.commented_text,
            'author_fname': latest_comment.author.first_name,
            'author_lname': latest_comment.author.last_name,
            'commentId': latest_comment.id,
            'parent_comment_id': latest_comment.parent_comment_id,
        }
        print("returednd")

        return JsonResponse(data_obj, safe=False)


"""This view gets called when the user clicks on the saved button in the navbar. This view will 
redirect the user to the page where he can see all the posts he has ever saved and if he wants he 
can remove the post from that list. The template of the view internally calls the ajax if the post 
is unsaved the ajax in turn calls the 'save_post' view whose url is in the 'Blogging/urls'  with name 
'save-post2' """


class SavedPostView(ListView, LoginRequiredMixin):
    model = Profile
    template_name = 'blog/saved_posts.html'
    context_object_name = 'saved_posts'

    def get_queryset(self):
        user = User.objects.filter(id=self.request.user.id).first()
        profile = Profile.objects.filter(user = user).first()

        return profile.saved_posts.all().order_by('-date')


@csrf_exempt
@login_required
def check_for_new_notification(request):
    if request.user.is_authenticated:
        new_notification = request.user.profile.notification.filter(status='new')
        total_notification = len(new_notification)
        if len(new_notification)>0:
            return JsonResponse(data={'newNotification':total_notification}, safe=False)
        return JsonResponse(data={'newNotification':total_notification}, safe=False)





# class AboutView(DetailView):
#     template_name = "blog/about.html"

# def about(request):
#     context = {
#         'posts': posts
#     }
#     return render(request, 'blog/about.html', context)


# singlePost = Post.objects.filter(id = pid).first()
#     if request.method  == 'POST':
#         comment_form = CommentForm(request.POST)

#         if comment_form.is_valid():
#             text = comment_form.cleaned_data['commented_text']
#             singlePost.comments.create(commented_post=singlePost, author=request.user,commented_text=text)
#         else:
#             print(comment_form.errors)

#     else:
#         comment_form = CommentForm()
    
#     return render(request, 'blog/singlePost.html', {
#             'singlePost': singlePost,
#             'comment_form': comment_form
#         })