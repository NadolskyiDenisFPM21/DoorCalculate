# Generated by Django 5.0.1 on 2024-02-14 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0017_alter_table_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='date',
            field=models.DateField(default='2024-02-14'),
        ),
    ]