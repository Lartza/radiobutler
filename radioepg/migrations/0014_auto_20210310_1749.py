# Generated by Django 3.1.7 on 2021-03-10 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('radioepg', '0013_auto_20210310_1747'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imageslide',
            old_name='url',
            new_name='image',
        ),
    ]