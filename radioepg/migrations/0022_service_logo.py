# Generated by Django 3.2 on 2021-04-14 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('radiovis', '0006_auto_20210414_1850'),
        ('radioepg', '0021_remove_service_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='logo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='radiovis.image'),
        ),
    ]