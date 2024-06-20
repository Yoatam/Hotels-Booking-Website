# Generated by Django 5.0.3 on 2024-03-26 12:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Memory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('image', models.FileField(default=None, max_length=2500, null=True, upload_to='user_memories/')),
                ('about', models.TextField()),
                ('date', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=40)),
                ('user_review', models.TextField()),
                ('ratings', models.IntegerField()),
            ],
        ),
    ]