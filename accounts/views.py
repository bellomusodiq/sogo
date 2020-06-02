from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, ProfileAndVRSerializer
from .models import ProfileAndVR
from django.contrib.auth.models import User

# Create your views here.


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()

        return queryset


class ProfileAndVRViewSet(ModelViewSet):
    serializer_class = ProfileAndVRSerializer
    queryset = ProfileAndVR.objects.all()


def jwt_response_payload_handler(token, user=None, request=None):
    return dict(token=token, userid=user.id)
