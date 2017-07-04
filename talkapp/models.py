from django.db import models
#ユーザー情報用モデルインポート
from django.contrib.auth.models import User

class Profile(models.Model):
    image = models.CharField(max_length=255)
    user = models.OneToOneField(User)

class PostMessage(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

