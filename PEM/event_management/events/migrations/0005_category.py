# Generated by Django 5.1.1 on 2024-12-04 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
