# Generated by Django 3.1.6 on 2021-02-11 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210211_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='code',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
