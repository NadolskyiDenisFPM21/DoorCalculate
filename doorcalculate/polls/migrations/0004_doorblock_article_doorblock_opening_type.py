# Generated by Django 5.0.1 on 2024-01-22 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_remove_doorblock_opening_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='doorblock',
            name='article',
            field=models.IntegerField(blank=True, default=-1, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='doorblock',
            name='opening_type',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
