# Generated by Django 2.2.6 on 2019-10-10 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charity', '0003_institution_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='is_taken',
            field=models.BooleanField(default=False),
        ),
    ]
