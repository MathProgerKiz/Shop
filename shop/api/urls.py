from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shop.api.views import OrderViewSet, ProductViewSet, ReviewViewSet
from users.api.views import UserViewSet

router = DefaultRouter()
router.register(r'product', ProductViewSet)

router_order = DefaultRouter()
router.register(r'order', OrderViewSet)

router_review = DefaultRouter()
router.register(r'review', ReviewViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('',include(router_order.urls)),
    path('',include(router_review.urls))
]
