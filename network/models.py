from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class UserFollowing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True)
    likes = models.ManyToManyField(User, related_name="liked_posts") 
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
    
    def serialize(self):
        return {
            "id": self.id,
            "likes": self.likes.all(),
            "body": self.body
        }