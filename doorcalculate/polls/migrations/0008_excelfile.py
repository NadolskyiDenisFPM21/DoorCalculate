# Generated by Django 5.0.1 on 2024-01-25 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_doorblock_is_primed'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
            ],
        ),
    ]
