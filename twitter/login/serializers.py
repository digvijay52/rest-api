from rest_framework import serializers

from . import models

class HelloSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=10)


class UserProfileSerialzer(serializers.ModelSerializer):

    class Meta:
        model = models.UserProfile
        fields = ('id','email','name','password')
        extra_kwargs = {'password':{'write_only':True}}
    
    
class TwitterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TwitterModel
        fields = ('id','User','Tweet','Likes')

class TwitEnterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TwitterModel
        fields = ('id','User','Tweet')

class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FollowingModel
        fields = ('User','Following')
        depth = 1

class PostFollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.FollowingModel
        fields = ('User','Following')
        

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TwitLike
        fields = ('Tweet','LikedBy')

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TwitComment
        fields = ('Tweet','Comment','CommentBy')


    