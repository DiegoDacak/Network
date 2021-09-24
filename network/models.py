from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import CharField, NullBooleanField
from django.utils import timezone

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.CharField(max_length=1000, default="Null")
    date = models.DateTimeField(default=timezone.now())
    like = models.IntegerField(default=0)

    def __str__(self):
        return f"User: {self.user} Post: {self.post}"

class Follow(models.Model):
    profile= models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="profile")
    follower= models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="follower")

    def __str__(self):
        return f"Profile: {self.profile} Follower: {self.follower}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name="post_like")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="user_like")

    def __str__(self):
        return f"Post: ({self.post}) Like: {self.user}"



