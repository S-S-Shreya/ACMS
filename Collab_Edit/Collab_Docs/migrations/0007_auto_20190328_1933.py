# Generated by Django 2.1.7 on 2019-03-28 14:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Collab_Docs', '0006_auto_20190326_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accept_reject',
            name='accept',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='accept_reject',
            name='reject',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 28, 19, 33, 12, 838705)),
        ),
    ]
