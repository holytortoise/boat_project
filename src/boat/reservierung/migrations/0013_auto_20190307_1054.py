# Generated by Django 2.0.6 on 2019-03-07 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservierung', '0012_auto_20190307_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instandsetzung',
            name='durchfuehrung_durch',
            field=models.CharField(default='Ausstehend', max_length=255, null=True),
        ),
    ]