from rest_framework import serializers
from django.core.exceptions import ValidationError

from shop.models import Order, Product, Review
from users.models import User


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['buyer', 'product']

    def create(self, validated_data):
        """ Проверка: не покупает ли пользователь свой  же товар """
        buyer = validated_data['buyer']
        product_from_order = validated_data['product']

        if product_from_order in buyer.products.all():
            raise ValidationError("Покупатель не может купить свой же товар!")

        order = Order.objects.create(
            buyer=buyer,
            product=product_from_order
        )
        return order


class ProductSerializers(serializers.ModelSerializer):

    def validate_price(self, value):
        """Валидатор проверяет цену на корректность """
        if value < 0:
            raise serializers.ValidationError("цена должна быть положительной")
        return value

    def validate_file(self, value):
        """Валидатор проверяет корректность типа для файла"""
        acceptable = ['ZIP', 'RAR', '7z', 'PDF', 'DOC', 'TXT']
        if not value in acceptable:
            raise serializers.ValidationError(
                "Файл должен быть допустимого типа")
        return value

    class Meta:
        model = Product
        fields = ['title', 'desription', 'price', 'file', 'seller']


class ReviewSerializers(serializers.ModelSerializer):
    def validate_rating(self, value):
        """ Проверка корректности выставления рейтинга"""
        if not 0 < value < 6:
            raise serializers.ValidationError(
                "Рейтинг должен быть от 1 до 5")
        return value

    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        """Проверка того может ли пользователь оставлять отзыв по товару"""
        buyer = validated_data['user']
        product = validated_data['product']
        if not product in buyer.product:
            raise ValidationError("Вы не покупали данный товар!")

        review = Review.objects.create(**validated_data)
        return review
