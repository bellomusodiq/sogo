from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
