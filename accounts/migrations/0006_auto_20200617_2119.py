# Generated by Django 3.0.5 on 2020-06-17 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200615_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(blank=True, default='default/person.png', upload_to='profile/'),
        ),
    ]