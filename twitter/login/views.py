# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import io
from collections import OrderedDict
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser 
from . import serializers,models,permissions
from rest_framework import status   
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListCreateAPIView



class HelloApiView(APIView):


    serializer_class = serializers.HelloSerializer


    def post(self, request):

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = "Hello {0}".format(name)

            return Response({'message':message} )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    def get(self, request, format=None):


        an_apiview = [
             'Uses HTTP Method as functions (get,post,patch,put,delete)',
             'It is similar to a traditional django view',
             'Gives you the most control over your logiv',
             'It is mapped manually to URLS',
         ]

        return Response({'message':'Hello','an_apiview':an_apiview})
    
    def put(self, request, pk=None):

        return Response({'message':'put'})
# Create your views here.

class HelloViewSet(viewsets.ViewSet):
    serializer_class = serializers.HelloSerializer

    def create(self, request):

        serializer = serializers.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = "Hello {0}".format(name)

            return Response({'message':message} )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    def list(self, request):

        a_viewset = [
            'Uses action (list, create, reetrieve, update, partial_update)',
            'Automatically maps urls using Routers',
            'Provides more functionality with less code'
        ]

        return Response({'message':'Hello!','a_viewset':a_viewset})

    

    def retrieve(self, request, pk=None):

        return Response({'http_method':'GET'})

class UserProfileApi(ListCreateAPIView):
    

    serializer_class= serializers.UserProfileSerialzer
    

    def get(self, request, id):
        if id == '':
            queryset= models.UserProfile.objects.all()
        else:         
            queryset= models.UserProfile.objects.all().filter(id=id)
        
        authentication_classes=(TokenAuthentication,)
        permission_classes=(permissions.UpdateOwnProfile,)
        filter_backends = (filters.SearchFilter,)
        search_fields = ('name','email', )
        serializer = serializers.UserProfileSerialzer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, id):
        data = JSONParser().parse(request)
        serializer = serializers.UserProfileSerialzer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Message":"Profile Added Succesfully"})
        else:
            return Response({"Message":"Error Encountered"})

   

class LoginViewApi(APIView):
    serializer_class = AuthTokenSerializer

    def get(self, request,format=None):

        an_apiview = [
             'LOGIN VIEW'
         ]

        return Response({'message':'Hello','an_apiview':an_apiview})
    
    def post(self,request):
        data = JSONParser().parse(request)
        # print(list(models.UserProfile.objects.all().filter(email=data["email"],password=data["password"])))
        if not list(models.UserProfile.objects.all().filter(email=data["email"],password=data["password"])):
            return Response({"Message":"Wrong Credentials"})
        else:
            return Response({"Message":"Succesfully Login Done"})
        
        




class TwitterAPI(APIView):
    serializer_class = serializers.TwitEnterSerializer

    def get(self, request, email):
        
        if email== '':
            queryset = models.TwitterModel.objects.all()
        else:
            print(email)
            queryset= models.UserProfile.objects.all().filter(email=email)
            User=serializers.UserProfileSerialzer(instance=queryset, many=True).data[0]["id"]
            print(User)
            queryset= models.TwitterModel.objects.all().filter(User=User)

        serializer = serializers.TwitterSerializer(queryset, many=True)

        return Response(serializer.data)

    def post(self, request, email,   format=None):
        data = JSONParser().parse(request)
        username=data["User"]
        queryset= models.UserProfile.objects.all().filter(email=username)
        tempdata=serializers.UserProfileSerialzer(instance=queryset, many=True).data
        data["User"]=tempdata[0]["id"]
        
        serializer = serializers.TwitEnterSerializer(data=data)
        

        if serializer.is_valid():
            serializer.save()
            Response = {"Output": "Succefully entered the data"}
        else:
            Response = {"Output": "Error Encountered"}
        return JsonResponse(Response)    

class FollowingAPI(APIView):

        serializer_class = serializers.FollowingSerializer

        def get(self, request, user):
            if user=='':
                queryset = models.FollowingModel.objects.all()
            else:
                user = models.UserProfile.objects.all().filter(email=user)
                queryset = models.FollowingModel.objects.all().filter(User=user)      
            serializer = serializers.FollowingSerializer(queryset,many =True)
            values = [[{"User":data["User"]["email"],"Following":data["Following"]["email"]}] for data in serializer.data]
                  
            return Response(values)
        
        def post(self, request, user, format=None):
            data = JSONParser().parse(request)
            print(data)
            User=data["User"]
            queryset=models.UserProfile.objects.all().filter(email=User)
            tempdata=serializers.UserProfileSerialzer(instance=queryset, many=True).data
            
            data["User"]=tempdata[0]["id"]
            
            Following=data["Following"]
            queryset=models.UserProfile.objects.all().filter(email=Following)
            tempdata=serializers.UserProfileSerialzer(instance=queryset, many=True).data
            data["Following"]=tempdata[0]["id"]
            print(data)
            serializer = serializers.PostFollowingSerializer(data=data)
            
            if serializer.is_valid():
                serializer.save()
                return Response({"Output": "Succefully Followed"})
            else:
                return Response( {"Output": "Error Encountered"})
            
            # return Response({"Output": "Error Encountered"})

class TwittFeed(APIView):
    serializer_class = serializers.TwitterSerializer

    def get(self, request, param):
        user = models.UserProfile.objects.all().filter(email=param)
        queryset = models.FollowingModel.objects.all().filter(User=user)
        serializer=serializers.FollowingSerializer(queryset, many=True)
        values = [data["Following"]["id"] for data in serializer.data]
        print(values)
        queryset = models.TwitterModel.objects.all().filter(User__in=values)
        serializer=serializers.TwitterSerializer(queryset, many=True)
        return Response(serializer.data)


class Likes(APIView):
    serializer_class = serializers.LikeSerializer

    def get(self, request):
        data = JSONParser().parse(request)
        queryset = models.TwitLike.objects.all().filter(Tweet=data["Tweet"])
        serializer = serializers.LikeSerializer(instance=queryset, many=True)
        return Response(serializer.data)
    

    def post(self, request):
        data = JSONParser().parse(request)
        if data["Action"]=="Like":
            data["LikedBy"]=models.UserProfile.objects.get(email=data["LikedBy"]).id
            print(data)
            data={"Tweet":data["Tweet"],"LikedBy":data["LikedBy"]}
            print(data)
            serializer=serializers.LikeSerializer(data=data)
            Tweet=models.TwitterModel.objects.get(id=data["Tweet"])
            if serializer.is_valid():
                    Tweet.Likes+=1
                    Tweet.save()
                    serializer.save()
                    return Response({"Output": "Succefully Liked"})
            else:
                    return Response( {"Output": "Error Encountered"})
        
        elif data["Action"]=="Dislike":
            LikedBy=models.UserProfile.objects.get(email=data["LikedBy"]).id

            if(models.TwitLike.objects.filter(Tweet=data["Tweet"],LikedBy=LikedBy).delete()[0]==1):
                Tweet=models.TwitterModel.objects.get(id=data["Tweet"])
                Tweet.Likes-=1
                Tweet.save()
                return Response({"Output": "Succefully Disliked"})
            else:
                return Response({"Output": "Error Encountered"})


class Comment(APIView):
    serializer_class = serializers.CommentSerializer

    def get(self, request):
        data = JSONParser().parse(request)
        queryset = models.TwitComment.objects.all().filter(Tweet=data["Tweet"])
        serializer = serializers.CommentSerializer(instance=queryset, many=True)
        return Response(serializer.data)
        

    def post(self, request):
        data = JSONParser().parse(request)
        if data["Action"]=="Comment":
            data["CommentBy"]=models.UserProfile.objects.get(email=data["CommentBy"]).id
            data={"Tweet":data["Tweet"],"Comment":data["Comment"],"CommentBy":data["CommentBy"]}
            serializer = serializers.CommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"Messgae":"Succefully Commented"})
            else:
                return Response({"Output": "Error Encountered"})
        
        if data["Action"]=="Delete":
            data["CommentBy"]=models.UserProfile.objects.get(email=data["CommentBy"]).id
            models.TwitComment.objects.filter(Tweet=data["Tweet"],Comment=data["Comment"],CommentBy=data["CommentBy"]).delete()
            return Response({"Message":"Succesfully Deleted"})

        
       

            


            
            







































