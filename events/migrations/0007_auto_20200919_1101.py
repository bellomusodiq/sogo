# Generated by Django 3.1 on 2020-09-19 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_auto_20200919_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='url',
            field=models.FileField(upload_to='events'),
        ),
        migrations.AlterField(
            model_name='eventartist',
            name='image',
            field=models.ImageField(upload_to='artist'),
        ),
        migrations.AlterField(
            model_name='eventimage',
            name='image',
            field=models.ImageField(upload_to='events-images'),
        ),
    ]
