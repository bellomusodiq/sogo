# Generated by Django 3.1 on 2020-10-10 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing_shop', '0007_auto_20201010_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='about',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='contact',
            name='message',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='privatepolicy',
            name='private_policy',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='termsofservice',
            name='terms_of_service',
            field=models.TextField(),
        ),
    ]
