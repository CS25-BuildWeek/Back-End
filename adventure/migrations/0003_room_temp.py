# Generated by Django 3.0.3 on 2020-02-06 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0002_auto_20200206_2225'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='temp',
            field=models.IntegerField(default=0),
        ),
    ]
