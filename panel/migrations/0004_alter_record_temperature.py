# Generated by Django 3.2.9 on 2022-03-25 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0003_alter_record_temperature'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='temperature',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]