# Generated by Django 4.2.6 on 2023-10-15 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_comment_replyto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='watching',
            field=models.ManyToManyField(to='auctions.listing'),
        ),
    ]