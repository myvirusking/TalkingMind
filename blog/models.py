from django.utils import timezone
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User
from users.models import ArticleCategory

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class CommentLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class PostImages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_pics',null=True)

    def __str__(self):
        return f"{self.user.username} - {self.image}"


class Comment(models.Model):
    commented_post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="commented_post")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    commented_text = models.TextField()
    cmt_likes = models.ManyToManyField(User)
    cmt_likes_count = models.PositiveIntegerField(default=0)
    comment_date = models.DateTimeField(default=timezone.now)
    parent_comment_id = models.PositiveIntegerField(default=0)
    flag = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-comment_date']

    def __str__(self):
        return self.author.username

   

   

   

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE,null=True)
    images = models.ManyToManyField(PostImages,null=True)
    likes = models.ManyToManyField(User, null=True, related_name='users_who_liked_post')
    likes_count = models.PositiveIntegerField(default=0)
    comments = models.ManyToManyField(Comment, null=True)
    comments_count = models.PositiveIntegerField(default=0)
    rank_score = models.FloatField(default=0.0)

    def __str__(self):
        return self.title

    def set_rank(self):
        SECS_IN_HOUR = float(60 * 60)
        GRAVITY = 1.2

        delta = now() - self.date_posted
        item_hour_age = delta.total_seconds() // SECS_IN_HOUR
        votes = self.likes - 1
        self.rank_score = votes / pow((item_hour_age + 2), GRAVITY)
        self.save()



    




