from django.contrib import admin
from .models import ArticleCategory,FollowRequest,Following,Followers

# Register your models here.

admin.site.register(ArticleCategory)
admin.site.register(FollowRequest)
admin.site.register(Followers)
admin.site.register(Following)

