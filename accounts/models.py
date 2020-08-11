from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import string
import random


class ProfileAndVR(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_image', blank=True, null=True)
    received_vr_headset = models.BooleanField(default=False)
    vr_email_address = models.EmailField(max_length=255, blank=True, null=True)
    vr_name = models.CharField(max_length=225, blank=True, null=True)
    vr_address = models.CharField(max_length=400, blank=True, null=True)
    vr_country = models.CharField(max_length=225, blank=True, null=True)
    vr_city = models.CharField(max_length=225, blank=True, null=True)
    vr_state = models.CharField(max_length=225, blank=True, null=True)
    vr_zip_code = models.CharField(max_length=225, blank=True, null=True)
    vr_phone_number = models.CharField(max_length=225, blank=True, null=True)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        ProfileAndVR.objects.create(
            user=instance
        )


class AccountResetLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=400, blank=True, null=True, unique=True)
    date_time = models.DateTimeField(auto_now_add=True)


def generate_token():
    token = ''
    for i in range(50):
        token += random.choice(string.ascii_letters + string.digits + string.hexdigits)
    return token


def reset_token(sender, instance, created, *args, **kwargs):
    if not instance.reset_token:
        instance.reset_token = generate_token()
        instance.save()


post_save.connect(reset_token, sender=AccountResetLink)
