# Generated by Django 5.0.1 on 2024-01-29 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_order_order_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.IntegerField(null=True),
        ),
    ]
