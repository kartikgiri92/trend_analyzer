# Generated by Django 2.2.9 on 2020-01-27 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prime', '0007_auto_20200127_0227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='compound_value',
            field=models.FloatField(default=0),
        ),
    ]