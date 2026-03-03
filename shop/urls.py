from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('about/', views.about, name = 'about'),
    path('shop/', views.shop_info, name = 'shop_info'),
    path('catalog/', views.product_list, name = 'product_list'), # Список товаров (каталог)
    path('catalog/<int:pk>/', views.product_detail, name = 'product_detail'), # Детальная информация о товаре по его ID
    path('cart/add/<int:product_id>/', views.cart_add, name = 'cart_add'), # Добавление товара в корзину
    path('cart/update/<int:item_id>/', views.cart_update, name = 'cart_update'), # Обновление количества товара в корзине
    path('cart/remove/<int:item_id>/', views.cart_remove, name = 'cart_remove'), # Удаление товара из корзины
    path('cart/', views.cart_view, name = 'cart_view'), # Просмотр корзины пользователя
]
