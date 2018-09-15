from django.db import models


class List(models.Model):
    pass


class Task(models.Model):
    text = models.TextField(default='')
    parent_list = models.ForeignKey(List, default=None)
