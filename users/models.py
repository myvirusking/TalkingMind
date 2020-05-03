from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from Blogging import settings


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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    about = models.CharField(max_length=150, default="I am using TalkingMind")
    article_category = models.ManyToManyField(ArticleCategory)
    followers = models.ManyToManyField(Followers, null=True)
    following = models.ManyToManyField(Following, null=True)

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







