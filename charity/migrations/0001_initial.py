# Generated by Django 2.2.6 on 2019-10-06 19:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('type', models.SmallIntegerField(choices=[(0, 'fundacja'), (1, 'organizacja pozarządowa'), (2, 'zbiórka lokalna')], default=0)),
                ('categories', models.ManyToManyField(to='charity.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField()),
                ('address', models.CharField(max_length=128)),
                ('phone_number', models.IntegerField()),
                ('city', models.CharField(max_length=128)),
                ('zip_code', models.CharField(max_length=10)),
                ('pick_up_date', models.DateField()),
                ('pick_up_time', models.DateTimeField()),
                ('pick_up_comment', models.TextField()),
                ('categories', models.ManyToManyField(to='charity.Category')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charity.Institution')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
