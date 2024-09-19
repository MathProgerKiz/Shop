from django.db import models

from users.models import User


class Order(models.Model):
    buyer = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='order',
                              blank=True
                              )
    product = models.ForeignKey('Product',
                                on_delete=models.CASCADE,
                                related_name='product',
                                )
    order_date = models.DateTimeField(auto_now_add=True,
                                      blank=True
                                      )


class Product(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    price=models.FloatField()
    file = models.CharField(max_length=128,default=None)  # тип продукта (в PDF ,ZIP)
    created_at = models.DateTimeField(auto_now_add=True,
                                      blank=True)
    update_at = models.DateTimeField(auto_now=True,
                                     blank=True)
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='products'
    )


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField()  # Используем PositiveSmallIntegerField для ограничения значения
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True,blank=True)