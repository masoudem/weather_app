# Generated by Django 3.2.9 on 2022-04-03 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0005_auto_20220326_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='created',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]