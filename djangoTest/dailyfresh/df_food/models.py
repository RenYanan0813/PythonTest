from django.db import models
from tinymce.models import H

# Create your models here.

class TypeInfo(models.Model):
    title = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=20)
    gpic = models.ImageField(upload_to='df_goods')
    gprice = models.DecimalField(max_length=5, decimal_places=2)
    isDelete = models.BooleanField(default= False)
    gunit = models.CharField(max_length=20, default='500g')
    gclick = models.IntegerField()
    gjanjie = models.CharField(max_length=200)
    gkucub = models.IntegerField()
    gcontent = HTMLfield()