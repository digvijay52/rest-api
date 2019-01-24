# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models

admin.site.register(models.UserProfile)
admin.site.register(models.TwitterModel)
admin.site.register(models.FollowingModel)
admin.site.register(models.TwitComment)
admin.site.register(models.TwitLike)
# Register your models here.

