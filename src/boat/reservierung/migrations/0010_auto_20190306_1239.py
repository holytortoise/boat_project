# Generated by Django 2.0.6 on 2019-03-06 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservierung', '0009_auto_20180802_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='boot',
            name='sperrung',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reservierung',
            name='anlegeplatz',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='reservierung',
            name='ziel',
            field=models.TextField(default=''),
        ),
    ]