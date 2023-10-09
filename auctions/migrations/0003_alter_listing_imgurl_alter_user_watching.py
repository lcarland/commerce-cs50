# Generated by Django 4.2.6 on 2023-10-09 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_alter_user_id_listing_comment_bid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='imgurl',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='watching',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.listing'),
        ),
    ]