# Generated by Django 5.0.1 on 2024-02-01 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_delete_excelfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doorblock',
            name='is_primed',
            field=models.CharField(max_length=50),
        ),
    ]
