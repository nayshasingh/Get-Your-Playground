# Generated by Django 3.2.8 on 2021-10-11 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turf', '0002_slotbooking'),
    ]

    operations = [
        migrations.AddField(
            model_name='slotbooking',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]