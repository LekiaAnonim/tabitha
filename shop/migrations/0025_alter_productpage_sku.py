# Generated by Django 4.2.13 on 2024-05-16 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_alter_productpage_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpage',
            name='SKU',
            field=models.CharField(default='1Qf2jBfAVsS', max_length=500),
        ),
    ]