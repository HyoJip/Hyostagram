# Generated by Django 3.0.5 on 2020-07-27 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20200727_0213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(default='settings.STATIC_URL/images/person.png', upload_to='profile'),
        ),
    ]
