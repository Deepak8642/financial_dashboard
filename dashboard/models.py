

from django.db import models 
from django.contrib.auth.models import User 
  
#Create mode for Expense 
class Expense(models.Model): 
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) 
    salary = models.IntegerField(default=0) 
    name = models.CharField(max_length=100, default='something') 
    price = models.IntegerField(default=0)
    targeted_item_cost = models.IntegerField(default=0)