from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import (ProductViewSet, CategoryViewSet, ManufacturerViewSet, CartViewSet, CartItemViewSet)

app_name = 'shop'

urlpatterns = [
    path('index/', views.index, name = 'index'),
    path('about/', views.about, name = 'about'),
    path('shop/', views.shop_info, name = 'shop_info'),
    path('catalog/', views.product_list, name = 'product_list'), # Список товаров (каталог)
    path('catalog/<int:pk>/', views.product_detail, name = 'product_detail'), # Детальная информация о товаре по его ID
    path('cart/add/<int:product_id>/', views.cart_add, name = 'cart_add'), # Добавление товара в корзину
    path('cart/update/<int:item_id>/', views.cart_update, name = 'cart_update'), # Обновление количества товара в корзине
    path('cart/remove/<int:item_id>/', views.cart_remove, name = 'cart_remove'), # Удаление товара из корзины
    path('cart/', views.cart_view, name = 'cart_view'), # Просмотр корзины пользователя
    path('accounts/', include('django.contrib.auth.urls')),
    path('checkout/', views.checkout, name='checkout'),
    path('', include(router.urls)),
]

# Создаем роутер и регистрируем ViewSets
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'manufacturers', ManufacturerViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)

