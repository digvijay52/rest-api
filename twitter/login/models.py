# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models



class UserProfile(models.Model):
    
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email    


class TwitterModel(models.Model):

    Tweet = models.CharField(max_length=150)
    User = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    Likes = models.IntegerField(default=0)

    def __str__(self):
        return self.Tweet


class FollowingModel(models.Model):

    User = models.ForeignKey(UserProfile, related_name="friends", on_delete=models.CASCADE)
    Following = models.ForeignKey(UserProfile, related_name="following", on_delete=models.CASCADE)

    class Meta:
        unique_together =("User","Following")

class TwitComment(models.Model):
    Tweet = models.ForeignKey(TwitterModel,on_delete=models.CASCADE)
    Comment = models.CharField(max_length=100)
    CommentBy = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

class TwitLike(models.Model):
    Tweet = models.ForeignKey(TwitterModel, on_delete=models.CASCADE)
    LikedBy = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        unique_together =("Tweet","LikedBy")

    def __str__(self):
        return '{0}'.format(self.Tweet)




    

# Create your models here.
