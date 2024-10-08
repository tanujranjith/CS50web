# Generated by Django 5.0.3 on 2024-07-12 03:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_likepost'),
    ]

    operations = [
        migrations.AddField(
            model_name='creatpost',
            name='likes',
            field=models.IntegerField(default=0, max_length=200),
        ),
        migrations.AlterField(
            model_name='likepost',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postliked', to='network.creatpost'),
        ),
    ]
