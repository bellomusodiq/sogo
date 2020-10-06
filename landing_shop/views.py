from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from .models import Landing, PrivatePolicy, TermsOfService, \
    Event, Contact, About, Product
from .serializers import LandingSerializer, PrivatePolicySerializer, TermsOfServiceSerializer, \
    EventSerializer, ContactSerializer, AboutSerializer, ProductSerializer
from rest_framework.views import APIView

# Create your views here.


class LandingView(APIView):

    def get(self, request):

        landing = Landing.objects.first()
        if not landing:
            return Response({'message': 'landing page data not found'}, 404)
        events = Event.objects.all()
        event_response = [EventSerializer(event).data for event in events]
        response = {
            'landing': LandingSerializer(landing).data,
            'events': event_response
        }
        return Response(response)


class FooterView(APIView):

    def get(self, request):

        landing = Landing.objects.first()
        if not landing:
            return Response({'message': 'landing page data not found'}, 404)
        response = {
            'twitter_url': landing.twitter_url,
            'facebook_url': landing.facebook_url,
            'instagram_url': landing.instagram_url,
            'linkedin_url': landing.linkedin_url,
            'location': landing.location,
            'info_email': landing.info_email,
            'support_email': landing.support_email,
            'phone': landing.phone,
        }
        return Response(response)


class TermsOfServiceView(APIView):

    def get(self, request):
        tos = TermsOfService.objects.first()
        if not tos:
            return Response({'message': 'terms of service was not found'}, 404)
        return Response(TermsOfServiceSerializer(tos).data)


class PrivatePolicyView(APIView):

    def get(self, request):
        tos = PrivatePolicy.objects.first()
        if not tos:
            return Response({'message': 'privacy policy was not found'}, 404)
        return Response(PrivatePolicySerializer(tos).data)


class AboutView(APIView):

    def get(self, request):
        tos = About.objects.first()
        if not tos:
            return Response({'message': 'about was not found'}, 404)
        return Response(AboutSerializer(tos).data)


class ContactViewSet(ModelViewSet):

    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


class ProductViewSet(ModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
