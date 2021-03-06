# Generated by Django 3.1.7 on 2021-03-28 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courier_id', models.IntegerField()),
                ('courier_type', models.CharField(max_length=30)),
                ('regions', models.TextField(max_length=469)),
                ('working_hours', models.CharField(max_length=255)),
                ('capacity', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField()),
                ('weight', models.FloatField()),
                ('region', models.IntegerField()),
                ('delivery_hours', models.CharField(max_length=255)),
                ('assign_time', models.CharField(default='-', max_length=30)),
                ('complete_time', models.CharField(default='-', max_length=30)),
            ],
        ),
    ]
