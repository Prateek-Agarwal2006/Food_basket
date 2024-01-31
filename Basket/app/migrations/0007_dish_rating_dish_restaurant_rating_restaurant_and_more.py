# Generated by Django 5.0.1 on 2024-01-31 04:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_basket_seller'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='rating_dish',
            field=models.ManyToManyField(related_name='dish_rating', through='app.Rating_dish', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='rating_restaurant',
            field=models.ManyToManyField(related_name='user_ratings_for_restaurant', through='app.Rating_restaurant', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='dish',
            name='new_order_by',
            field=models.ManyToManyField(related_name='order', through='app.Order', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='rating_dish',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dish_rating', to='app.dish'),
        ),
        migrations.AlterField(
            model_name='rating_restaurant',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant_user_ratings', to='app.restaurant'),
        ),
        migrations.AlterField(
            model_name='rating_restaurant',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_restaurant_ratings', to=settings.AUTH_USER_MODEL),
        ),
    ]
