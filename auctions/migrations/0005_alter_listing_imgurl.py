# Generated by Django 4.2.6 on 2023-10-15 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_user_watching'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='imgurl',
            field=models.CharField(default='/static/auctions/product-placeholder.jpg', max_length=200),
        ),
    ]
