# Generated by Django 5.0.1 on 2024-03-04 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0018_alter_table_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='doorblock',
            name='opening_type2',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='table',
            name='date',
            field=models.DateField(default='2024-03-04'),
        ),
    ]
