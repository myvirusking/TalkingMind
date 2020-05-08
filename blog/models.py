from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from users.models import ArticleCategory

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to='post_pics',null=True)
    likes = models.ManyToManyField(Likes, null=True)
    likes_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title







