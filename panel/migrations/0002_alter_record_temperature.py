# Generated by Django 3.2.9 on 2022-03-25 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='temperature',
            field=models.FloatField(null=True),
        ),
    ]
