# Generated by Django 4.2.13 on 2024-05-16 11:44

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_importantpages_privacy'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitelogo',
            name='sign_in_image',
            field=cloudinary.models.CloudinaryField(blank=True, help_text='Upload image that appears on the login page', max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AddField(
            model_name='sitelogo',
            name='sign_up_image',
            field=cloudinary.models.CloudinaryField(blank=True, help_text='Upload image that appears on the signup page', max_length=255, null=True, verbose_name='image'),
        ),
    ]
