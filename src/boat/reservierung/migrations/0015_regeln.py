# Generated by Django 2.0.6 on 2019-03-08 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservierung', '0014_auto_20190307_1115'),
    ]

    operations = [
        migrations.CreateModel(
            name='Regeln',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regel', models.TextField(default='N/A')),
            ],
        ),
    ]
