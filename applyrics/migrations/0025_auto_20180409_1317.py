# Generated by Django 2.0.3 on 2018-04-09 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applyrics', '0024_auto_20180409_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submittedlyrics',
            name='replaced_new_lines',
            field=models.BooleanField(),
        ),
    ]