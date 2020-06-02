from django.db import models
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Event(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100, choices=(('live', 'live'), ('360videos', '360videos')))
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=400)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    details = models.TextField()
    image = models.ImageField(upload_to='events')
    url = models.URLField()
    is_live = models.BooleanField(default=False)


class EventImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events')


class EventArtist(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='artist')
    name = models.CharField(max_length=400)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=400)
    date = models.DateField(auto_now_add=True)

    class Meta:
        get_latest_by = ['-date']


class MyTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
