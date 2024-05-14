from django.contrib.auth.models import User
from django.db import models

from product.models import Product

class Order(models.Model):
    status_choices = [
        ('Pending', 'PENDING'),
        ('Completed', 'COMPLETED'),
    ]

    payment_method_choices = [
        ('Airtel', 'AIRTEL'),
        ('MTN', 'MTN'),
        ('Card', 'CARD'),
        ('Cash', 'CASH'),
    ]
    
    status = models.CharField(max_length=10, choices=status_choices, default='Pending')
    payment_method = models.CharField(max_length=50, choices=payment_method_choices)
    ordered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_ordered_by")
    ordered_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_created_by")

    def __str__(self):
        return f"Order {self.id} ({self.ordered_on})"

class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_item_order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_item_product")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calc_total(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        self.unit_price = self.product.selling_price
        self.total = self.calc_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order.id} ({self.order.ordered_on}) - {self.product.name} [{self.quantity}/{self.unit_price}][{self.total}]"