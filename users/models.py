from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image


class SavedPost(models.Model):
    post = models.ForeignKey("blog.Post", on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)


class ArticleCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Followers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class Notification(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    notification_title = models.CharField(max_length=100)
    notification_type = models.CharField(max_length=100, null=True)
    notification_content = models.CharField(max_length=100, null=True)
    post_involved = models.ForeignKey("blog.Post",on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length = 100, default="new")  


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    bio = models.CharField(max_length=100, default="I am using TalkingMind")
    about = models.CharField(max_length=400, default="I am using TalkingMind")
    article_category = models.ManyToManyField(ArticleCategory)
    followers = models.ManyToManyField(Followers)
    following = models.ManyToManyField(Following)
    blocked_users = models.ManyToManyField(User, null=True, related_name="blocked_users")
    blocked_by = models.ManyToManyField(User, null=True, related_name="blocked_by")
    following_count = models.PositiveIntegerField(default=0)
    followers_count = models.PositiveIntegerField(default=0)
    saved_posts = models.ManyToManyField(SavedPost)
    saved_posts_count = models.PositiveIntegerField(default=0)
    notification = models.ManyToManyField(Notification)
    notification_count = models.PositiveIntegerField(default=0)
    mobile_no = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)

            img.thumbnail(output_size)
            img.save(self.image.path)


class FollowRequest(models.Model):
    from_user = models.ForeignKey(User,related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User,related_name='to_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)







