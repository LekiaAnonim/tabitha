from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, InlinePanel, FieldRowPanel, MultiFieldPanel, PageChooserPanel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    country = models.CharField(verbose_name='country', max_length=255, null=True, blank=True)
    region = models.CharField(verbose_name='region', max_length=255, null=True, blank=True)
    # status = models.ForeignKey(MembershipStatus, on_delete=models.SET_NULL, null=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    residential_address = models.CharField(max_length=255, null=True, blank=True)
    avatar = CloudinaryField("image", null=True, blank=True)

    def get_absolute_url(self):
        return reverse('shop:account')