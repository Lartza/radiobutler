# Generated by Django 3.2 on 2021-04-14 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('radiovis', '0005_auto_20210407_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='image112',
            field=models.ImageField(default='unavailable', upload_to='scaled'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='image128',
            field=models.ImageField(default='unavailable', upload_to='scaled'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='image32',
            field=models.ImageField(default='unavailable', upload_to='scaled'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='image320',
            field=models.ImageField(default='unavailable', upload_to='scaled'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='image600',
            field=models.ImageField(default='unavailable', upload_to='scaled'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
