# Generated by Django 5.1.1 on 2024-12-06 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_event_quantity_event_user_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='total_price',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]