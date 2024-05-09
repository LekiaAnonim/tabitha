# Generated by Django 5.0.4 on 2024-05-04 13:27

import cloudinary.models
import django.db.models.deletion
import modelcluster.fields
import wagtail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0093_uploadedfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='CategoryPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('category_name', models.CharField(blank=True, help_text='Enter a product category', max_length=500, null=True)),
                ('category_description', wagtail.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ProductIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ProductPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('product_name', models.CharField(blank=True, max_length=500, null=True)),
                ('original_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('on_sale', models.BooleanField(default=True)),
                ('image1', cloudinary.models.CloudinaryField(blank=True, help_text='Enter first product image', max_length=255, null=True, verbose_name='image')),
                ('image2', cloudinary.models.CloudinaryField(blank=True, help_text='Enter second product image', max_length=255, null=True, verbose_name='image')),
                ('image3', cloudinary.models.CloudinaryField(blank=True, help_text='Enter third product image', max_length=255, null=True, verbose_name='image')),
                ('short_description', models.CharField(blank=True, max_length=1000, null=True)),
                ('full_description', wagtail.fields.RichTextField(blank=True, null=True)),
                ('product_category', modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_category', to='shop.categorypage')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
