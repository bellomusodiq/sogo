"""sogo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from accounts.views import UserViewSet
from events.views import (
    CategoryViewSet, NotificationViewSet,
    EventViewSet, EventArtistViewSet
)

router = routers.DefaultRouter()

router.register('user', UserViewSet, 'user')
router.register('category', CategoryViewSet, 'category')
router.register('notifications', NotificationViewSet, 'notifications')
router.register('events', EventViewSet, 'events')
router.register('event-artist', EventArtistViewSet, 'event-artist')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
