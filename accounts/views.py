from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from django.contrib.auth.models import User

# Create your views here.


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()

        return queryset
