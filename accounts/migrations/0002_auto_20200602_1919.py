# Generated by Django 3.0.6 on 2020-06-02 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileandvr',
            name='vr_address',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='profileandvr',
            name='vr_city',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AddField(
            model_name='profileandvr',
            name='vr_country',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AddField(
            model_name='profileandvr',
            name='vr_email_address',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profileandvr',
            name='vr_name',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AddField(
            model_name='profileandvr',
            name='vr_phone_number',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AddField(
            model_name='profileandvr',
            name='vr_state',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
        migrations.AddField(
            model_name='profileandvr',
            name='vr_zip_code',
            field=models.CharField(blank=True, max_length=225, null=True),
        ),
    ]
