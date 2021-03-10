# Generated by Django 3.1.6 on 2021-02-22 11:34

from django.db import migrations, models
import radioepg.storage


class Migration(migrations.Migration):

    dependencies = [
        ('radioepg', '0007_auto_20210222_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='logo',
            field=models.ImageField(null=True, storage=radioepg.storage.OverwriteStorage(), upload_to='logos/'),
        ),
    ]