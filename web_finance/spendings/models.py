from django.db import models
from django.contrib.auth.models import User

class categories(models.Model):
    description = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.description}"

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

class spendings(models.Model):
    date = models.DateTimeField()
    amount = models.FloatField()
    category = models.ForeignKey(categories, null=True, on_delete=models.SET_NULL)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"ID({self.id}): {self.date} {self.amount} {self.category} {self.user}" 

    class Meta:
        verbose_name = 'spending'
        verbose_name_plural = 'spendings'