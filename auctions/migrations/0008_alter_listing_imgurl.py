# Generated by Django 4.2.6 on 2023-10-12 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_listing_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='imgurl',
            field=models.CharField(default='https://scotturb.com/wp-content/uploads/2016/11/product-placeholder.jpg', max_length=200, null=True),
        ),
    ]