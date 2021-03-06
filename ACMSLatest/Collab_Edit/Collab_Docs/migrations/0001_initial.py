# Generated by Django 2.1.5 on 2019-03-19 11:03

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docID', models.DateTimeField(default=django.utils.timezone.now)),
                ('version', models.FloatField(default=1.0)),
                ('docname', models.CharField(max_length=50)),
                ('content', django_mysql.models.JSONField(default=dict)),
                ('lock', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='LatestVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docVersionID', models.IntegerField()),
                ('latestVersion', models.FloatField(default=1.0)),
            ],
        ),
        migrations.CreateModel(
            name='User_Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ROLE', models.CharField(choices=[('COLLABORATOR', 'C'), ('REVIEWER', 'R')], default='COLLABORATOR', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('LOGIN_ID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('PASSWORD', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=30)),
                ('institution', models.CharField(max_length=50)),
                ('profession', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='user_document',
            name='LOGIN_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Collab_Docs.Users'),
        ),
        migrations.AddField(
            model_name='user_document',
            name='docID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Collab_Docs.Documents'),
        ),
        migrations.AlterUniqueTogether(
            name='documents',
            unique_together={('docID', 'version')},
        ),
        migrations.AlterUniqueTogether(
            name='user_document',
            unique_together={('docID', 'LOGIN_ID')},
        ),
    ]
