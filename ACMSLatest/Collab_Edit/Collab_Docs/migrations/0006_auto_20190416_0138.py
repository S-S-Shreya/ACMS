# Generated by Django 2.1.5 on 2019-04-15 20:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Collab_Docs', '0005_auto_20190416_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 16, 1, 38, 4, 387078)),
        ),
    ]