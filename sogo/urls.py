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
    EventViewSet, EventArtistViewSet,
    MyTicketViewSet, BookTicketAPIView
)
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter()

router.register('user', UserViewSet, 'user')
router.register('category', CategoryViewSet, 'category')
router.register('notifications', NotificationViewSet, 'notifications')
router.register('events', EventViewSet, 'events')
router.register('event-artist', EventArtistViewSet, 'event-artist')
router.register('my-tickets', MyTicketViewSet, 'my-tickets')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', obtain_jwt_token),
    path('api/verify-token/', verify_jwt_token),
    path('api/book-ticket/', BookTicketAPIView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
