from django.contrib.auth.models import User
from django.db import models

from product.models import Product

class Expense(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_product")
    quantity = models.IntegerField(default=1)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_created_by")
    add_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} ({self.add_on})"