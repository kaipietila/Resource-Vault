# Generated by Django 3.1.7 on 2021-03-19 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20210319_0517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apievent',
            name='error_details',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
