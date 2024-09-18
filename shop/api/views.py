from argparse import Action
from rest_framework.response import Response
from rest_framework import viewsets, status
from drf_spectacular.utils import extend_schema
from shop.api.serializers import OrderSerializers, ProductSerializers, ReviewSerializers
from shop.models import Order, Product, Review
from rest_framework.decorators import action


@extend_schema(tags=['Order'])
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializers
    queryset = Order.objects.all()


@extend_schema(tags=['Product'])
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializers
    queryset = Product.objects.all()

    @action(detail=True, methods=['get'])
    def rating(self, request):
        product_id = request.data['id']

        product_review = Product.objects.get(
            product_id).prefetch_related('reviews')

        result = 0
        for rating in product_review:
            result += rating.rating

        # Вычисляем рейтинг до 2 знаков после запятой
        result = (result/len(product_review))/100

        return Response({'Средний рейтинг': f'{result}'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Review'])
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializers
    queryset = Review.objects.all()
