# Generated by Django 2.0.3 on 2018-04-01 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applyrics', '0016_submittedlyrics_writer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submittedlyrics',
            name='date',
            field=models.DateField(),
        ),
    ]
