# Generated by Django 4.2.6 on 2023-10-18 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_listing_imgurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='sender',
            field=models.CharField(default='SysAdmin', max_length=64),
        ),
    ]