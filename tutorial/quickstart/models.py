from django.db import models

# Create your models here.
class DataRow(models.Model):
    content = models.CharField(max_length=5000)
    pass


class DataSet(models.Model):
    name = models.CharField(max_length=30, default='')
    rows = models.ManyToManyField(DataRow)