from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='title')
    content = models.TextField(verbose_name='content')
    image = models.ImageField(verbose_name='image', null=True, blank=True)
    view_count = models.IntegerField(null=True, blank=True, verbose_name='view_count')
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='date')