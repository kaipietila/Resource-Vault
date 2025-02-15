# Generated by Django 3.1.6 on 2021-02-11 18:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_auto_20210208_2053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resource',
            name='contributor',
        ),
        migrations.AddField(
            model_name='resource',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(upload_to='images'),
        ),
        migrations.DeleteModel(
            name='Contributor',
        ),
    ]
