# Generated by Django 5.0.4 on 2024-05-09 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_order_address_alter_order_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
    ]
