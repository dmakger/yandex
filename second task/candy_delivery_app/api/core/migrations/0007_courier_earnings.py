# Generated by Django 3.1.7 on 2021-03-28 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_order_lead_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='courier',
            name='earnings',
            field=models.FloatField(default=0),
        ),
    ]