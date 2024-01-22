# Generated by Django 5.0.1 on 2024-01-19 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DoorBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=50)),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('opening_type', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
            ],
        ),
    ]
