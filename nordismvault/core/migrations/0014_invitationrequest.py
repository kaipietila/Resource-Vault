# Generated by Django 3.1.7 on 2021-03-19 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_apievent_action'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvitationRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=128)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('invited', models.BooleanField(default=False)),
            ],
        ),
    ]
