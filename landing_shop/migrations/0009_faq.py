# Generated by Django 3.1 on 2020-10-12 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing_shop', '0008_auto_20201010_1922'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=400)),
                ('answer', models.TextField()),
            ],
        ),
    ]
