# Generated by Django 2.2.6 on 2020-12-17 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('page', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='page_likes', to='account.Profile'),
        ),
    ]
