"""
URL configuration for my_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import (ProductViewSet, CategoryViewSet, ManufacturerViewSet, CartViewSet, CartItemViewSet)
from django.conf import settings
from django.conf.urls.static import static
from .views import index, catalog

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
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('catalog/', catalog, name='catalog'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Создаем роутер и регистрируем ViewSets
router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'manufacturers', ManufacturerViewSet)
router.register(r'carts', CartViewSet)
router.register(r'cart-items', CartItemViewSet)
