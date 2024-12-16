from django.db import models
from datetime import date
# Create your models here.

class task(models.Model):
    name = models.CharField(max_length=200,default='Task')
    description = models.CharField(max_length=200, blank=False)
    input_data = models.CharField(max_length=200, blank=False)
    output_data = models.CharField(max_length=200, blank=False)
    date_create = models.DateField(auto_now_add=True)
    is_choice = models.BooleanField(default=False)

class User(models.Model):
    name = models.CharField(max_length=30,blank=False)
    email = models.CharField(max_length=200,blank=False)
    password = models.CharField(max_length=200, blank=False)
    is_admin = models.BooleanField(blank=False, default=False)