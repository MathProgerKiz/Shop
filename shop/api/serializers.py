from rest_framework import serializers
from django.core.exceptions import ValidationError

from shop.models import Order
from users.models import User


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['buyer', 'product']

    def create(self, validated_data):
        """ Проверка: покупает ли пользователь свой товар """
        buyer = validated_data['buyer']
        product_from_order = validated_data['product']

        if product_from_order in buyer.products.all():
            raise ValidationError("Покупатель не может купить свой же товар!")

        order = Order.objects.create(
            buyer=buyer,
            product=product_from_order
        )
        return order
