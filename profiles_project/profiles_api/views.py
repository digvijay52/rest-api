# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response    
from . import serializers
from rest_framework import status

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

