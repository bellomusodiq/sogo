from django.shortcuts import render
from .models import Category, Notification, EventArtist, Event, MyTicket, \
    EventImage
from .serializers import CategorySerializer, NotificationSerializer, \
    EventArtistSerializer, EventSerializer, MyTicketSerializer, \
    EventImageSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from .verify_payment import verify_transaction
from rest_framework import validators, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import timedelta


# Create your views here.


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000


class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.GET.get('user')
        queryset = Notification.objects.all()
        if user:
            queryset = queryset.filter(user__pk=user)

        return queryset


class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    pagination_class = StandardResultsSetPagination

    def get_serializer_context(self):
        context = super(EventViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        print(context)
        return context
    
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
        upcoming = self.request.GET.get('upcoming')
        if upcoming and (upcoming == 'true'):
            queryset = queryset.filter(date__gte=timezone.now())
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__id=category)
        date = self.request.GET.get('date')
        if date:
            queryset = queryset.filter(date=date)
        special_date = self.request.GET.get('special_date')
        if special_date and (special_date == 'today'):
            queryset = queryset.filter(date=timezone.now())
        if special_date and (special_date == 'tomorrow'):
            queryset = queryset.filter(date=timezone.now() + timedelta(days=1))
        # if special_date and (special_date == 'weekend'):
        #     current_date = timezone.now()
        #     if (current_date.weekday() == 5) or (current_date.weekday() == 6):
        #         queryset = queryset.filter()
        location = self.request.GET.get('location')
        if location:
            queryset = queryset.filter(location__icontains=location)
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

    def get_serializer_context(self):
        context = super(MyTicketViewSet, self).get_serializer_context()
        context.update({"request": self.request})
        print(context)
        return context


class EventImageViewSet(ModelViewSet):
    serializer_class = EventImageSerializer

    def get_queryset(self):
        queryset = EventImage.objects.all()

        event = self.request.GET.get('event')
        if event:
            queryset = queryset.filter(event=event)
        return queryset
