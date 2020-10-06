# Generated by Django 3.1 on 2020-10-04 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing_shop', '0003_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('image', models.ImageField(upload_to='shop/products')),
                ('price', models.FloatField()),
            ],
        ),
    ]
