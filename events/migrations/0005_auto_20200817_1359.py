# Generated by Django 2.2 on 2020-08-17 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_eventimage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ['-date']},
        ),
    ]
