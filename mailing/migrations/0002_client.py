# Generated by Django 4.2.4 on 2023-09-05 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('full_name', models.CharField(max_length=100)),
                ('comment', models.TextField()),
            ],
        ),
    ]