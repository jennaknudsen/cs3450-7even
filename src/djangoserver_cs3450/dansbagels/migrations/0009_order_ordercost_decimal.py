# Generated by Django 3.1.3 on 2020-11-19 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dansbagels', '0008_order_orderinstructions_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='orderCost_decimal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4),
        ),
    ]
