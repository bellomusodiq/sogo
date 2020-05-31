from rest_framework import serializers
from .models import Event, EventArtist, Category, Notification, MyTicket


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class EventArtistSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = EventArtist


class EventSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    artists = serializers.SerializerMethodField()

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
