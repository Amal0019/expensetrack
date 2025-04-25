# models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Expense(models.Model):
     name = models.CharField(max_length=100)
     amount = models.DecimalField(max_digits=10, decimal_places=2)
     category = models.ForeignKey(Category, on_delete=models.CASCADE)
     description = models.TextField()
     date = models.DateField()
     def __str__(self):
        return self.name



