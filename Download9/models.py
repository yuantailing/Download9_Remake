from django.db import models

# Create your models here.

class account(models.Model):
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40)

class task(models.Model):
    username = models.CharField(max_length=40)
    gid = models.CharField(max_length=40)
    taskname = models.CharField(max_length=40)