from django.shortcuts import render
from .models import Category, Notification, EventArtist, Event
from .serializers import CategorySerializer, NotificationSerializer, EventArtistSerializer, EventSerializer
from rest_framework.viewsets import ModelViewSet
# Create your views here.


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.GET.get('user')
        queryset = Notification.objects.all()
        if user:
            queryset = queryset.filter(user__pk=user)

        return queryset


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = Event.objects.all()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(title__icontains=q)
        return queryset


class EventArtistViewSet(ModelViewSet):
    serializer_class = EventArtistSerializer

    def get_queryset(self):
        queryset = EventArtist.objects.all()
        event = self.request.GET.get('event')
        if event:
            queryset = queryset.filter(event__pk=event)
        return queryset
