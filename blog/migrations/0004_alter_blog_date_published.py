# Generated by Django 4.2.4 on 2023-09-09 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blog_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='date_published',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date'),
        ),
    ]
