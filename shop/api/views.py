from rest_framework.response import Response
from rest_framework import viewsets, status
from drf_spectacular.utils import extend_schema
from shop.api.serializers import OrderSerializers, ProductSerializers, ReviewSerializers
from shop.models import Order, Product, Review
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from shop.permissions import IsAuthorOrReadOnly


@extend_schema(tags=['Order'])
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializers
    queryset = Order.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['order_date']

    @action(detail=False, methods=['get'])
    def my_order(self, request):
        user = request.user
        return Response({"Ваши заказы": len(user.order.all())}, status=status.HTTP_200_OK)


@extend_schema(tags=['Product'])
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializers
    queryset = Product.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['price', 'file', 'title', 'created_at', 'seller']

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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating']

    @action(detail=True, methods=['get'])
    def order_reviews(self, request):
        product_id = request.data['id']

        reviews_for_order = Product.objects.get(
            pk=product_id).prefetch_related('reviews')
        if reviews_for_order.reviews.all().exists():

            return Response({"Все отзывы по данному продукту": list(reviews_for_order.reviews.all())},
                            status=status.HTTP_200_OK)
        return Response({'detail': 'По данному товару нет отзывов'},
                        status=status.HTTP_200_OK)
