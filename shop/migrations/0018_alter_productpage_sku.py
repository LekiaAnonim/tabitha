# Generated by Django 5.0.4 on 2024-05-14 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_productpage_quantity_alter_productpage_sku'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productpage',
            name='SKU',
            field=models.CharField(default='3mli9e2leux', max_length=500),
        ),
    ]