# Generated by Django 3.1.7 on 2021-03-28 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210328_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='lead_time',
            field=models.CharField(default='-', max_length=30),
        ),
    ]
