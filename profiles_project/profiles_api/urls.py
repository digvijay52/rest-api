
from django.conf.urls import url,include
from . import views
from models import UserProfile
from . import serializers

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')



urlpatterns = [
    url(r'^profile/(?P<id>\d*)',views.UserProfileApi.as_view(queryset=UserProfile.objects.all())),
    url(r'^login/',views.LoginViewApi.as_view()),
    url(r'^hello-view/',views.HelloApiView.as_view()),  
    url(r'',include(router.urls))
]
