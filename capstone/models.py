from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Channel(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="watchlist",default=None)
    title = models.CharField(max_length=2000)
    img = models.CharField(max_length=2000)
    subs = models.IntegerField()
    views = models.IntegerField()
    videos = models.IntegerField()
    channel_id = models.CharField(max_length=2000)

