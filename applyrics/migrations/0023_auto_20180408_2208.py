# Generated by Django 2.0.3 on 2018-04-08 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applyrics', '0022_lyrics_remarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lyrics',
            name='remarks',
            field=models.CharField(max_length=100),
        ),
    ]
