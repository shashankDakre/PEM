# Generated by Django 5.1.1 on 2024-12-06 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_event_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]