from rest_framework import serializers
from .models import Event, EventArtist, Category, \
    Notification, MyTicket, EventImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = EventImage


class EventArtistSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = EventArtist


class EventSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    artists = serializers.SerializerMethodField()
    other_images = serializers.SerializerMethodField()
    paid = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Event

    def get_category_name(self, obj):
        return obj.category.name

    def get_artists(self, obj):
        artists = []
        for artist in obj.eventartist_set.all():
            artists.append(EventArtistSerializer(artist).data)
        return artists

    def get_other_images(self, obj):
        other_images = []
        for image in obj.eventimage_set.all():
            other_images.append(EventImageSerializer(image).data)
        return other_images

    def get_paid(self, obj, *args, **kwargs):
        val = False
        request = self.context.get('request')
        my_tickets = MyTicket.objects.filter(user=request.user)
        try:
            confirmed_ticket = my_tickets.get(user=request.user, event=obj)
            val = True
        except MyTicket.DoesNotExist:
            pass
        return val


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Notification


class MyTicketSerializer(serializers.ModelSerializer):
    event_details = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = MyTicket

    def get_event_details(self, obj):
        return EventSerializer(obj.event).data
