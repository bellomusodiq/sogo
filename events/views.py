from django.shortcuts import render
from .models import Category, Notification, EventArtist, Event, MyTicket
from .serializers import CategorySerializer, NotificationSerializer, \
    EventArtistSerializer, EventSerializer, MyTicketSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from .verify_payment import verify_transaction
from rest_framework import validators, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


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


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = Event.objects.all()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(title__icontains=q)
        live = self.request.GET.get('live')
        if live and (live == 'true'):
            queryset = queryset.filter(is_live=True)
        completed = self.request.GET.get('completed')
        if completed and (completed == 'true'):
            queryset = queryset.filter(date__lt=timezone.now())
        event_type = self.request.GET.get('type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        return queryset


class EventArtistViewSet(ModelViewSet):
    serializer_class = EventArtistSerializer

    def get_queryset(self):
        queryset = EventArtist.objects.all()
        event = self.request.GET.get('event')
        if event:
            queryset = queryset.filter(event__pk=event)
        return queryset


class BookTicketAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ref = request.data.get('ref')
        event = request.data.get('event')
        errors = {}
        if not ref:
            errors['ref'] = 'ref values is required'
        if not event:
            errors['event'] = 'event values is required'
        try:
            event_obj = Event.objects.get(pk=event)
            if len(errors) > 0:
                raise validators.ValidationError(errors)
            result = verify_transaction(ref)
            if result['status']:
                Notification.objects.create(
                    user=request.user,
                    message='You have successfully subscribed to {}'.format(event_obj.title)
                )
                MyTicket.objects.create(user=request.user, event=event_obj)
                return Response({'message': 'payment was successful'})
            return Response({'message': 'payment was not successful'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Event.DoesNotExist:
            raise validators.ValidationError({'event': 'event with the id does not exist'})


class MyTicketViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MyTicketSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = MyTicket.objects.all()
        user = self.request.GET.get('user')
        if user and (user == 'true'):
            queryset = queryset.filter(user=self.request.user)
        return queryset
