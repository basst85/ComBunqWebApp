from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models

# Create your models here.
class transactions(models.Model):
    """docstring for transactions."""
    attrs = JSONField()
    catagory = JSONField()
    
class catagories(models.Model):
    Naam = models.CharField(max_length=10)
    Rekening = ArrayField(models.CharField(max_length = 34), blank = True)
    
    def __str__(self):
        return self.Naam
    
        
