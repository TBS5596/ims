from django.contrib.auth.models import User
from django.db import models

from product.models import Product

class Stock(models.Model):
    ref_type_choices = [
        ('expense', 'EXPENSE'),
        ('order', 'ORDER')
    ]
    
    ref_type = models.CharField(max_length=10, choices=ref_type_choices)
    ref_id = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_product")
    quantity = models.IntegerField(default=1)
    add_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return {self.name}