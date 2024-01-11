from django.db import models
from .storage import OverwriteStorage

import datetime

# Create your models here.
class Report(models.Model):
    file=models.FileField(upload_to='',storage=OverwriteStorage())
    file_name=models.CharField(max_length=150,editable=False)
    created=models.DateTimeField(auto_now_add=True)
    is_approved = models.IntegerField(default=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    remarks = models.CharField(max_length=1000, null=True, default=None, blank=True)
    created_by=models.CharField(max_length=50,null=True,editable=False,default=None)
    updated_by=models.CharField(max_length=50,null=True,editable=False,default=None)
    # Signal receiver function
    

class create_user(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=100)