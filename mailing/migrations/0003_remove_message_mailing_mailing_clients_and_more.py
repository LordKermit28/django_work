# Generated by Django 4.2.4 on 2023-09-05 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_client'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='mailing',
        ),
        migrations.AddField(
            model_name='mailing',
            name='clients',
            field=models.ManyToManyField(to='mailing.client'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='messages',
            field=models.ManyToManyField(to='mailing.message'),
        ),
    ]