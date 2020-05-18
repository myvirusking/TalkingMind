from django.contrib import admin
from .models import Post, Likes,PostImages, Comment
from users.models import Profile, ArticleCategory, Followers, Following, FollowRequest

# Register your models here
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Likes)
admin.site.register(ArticleCategory)
admin.site.register(Followers)
admin.site.register(Following)
admin.site.register(FollowRequest)
admin.site.register(PostImages)
admin.site.register(Comment)
