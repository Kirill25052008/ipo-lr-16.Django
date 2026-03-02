from django.contrib.auth.models import User
from shop.models import Category, Manufacturer, Product, Cart, CartItem
import random

# Создаем 5 производителей
mans = []
for i in range(1, 6):
    m = Manufacturer.objects.create(name=f"Бренд {i}", country="Страна", description="Описание")
    mans.append(m)

# Создаем 10 категорий
cats = []
for i in range(1, 11):
    c = Category.objects.create(name=f"Категория {i}")
    cats.append(c)

# Создаем 34 товара
prods = []
for i in range(1, 35):
    p = Product.objects.create(
        name=f"Товар №{i}",
        description="Подробное описание товара",
        price=random.randint(100, 5000),
        stock_quantity=random.randint(10, 50),
        category=random.choice(cats),
        manufacturer=random.choice(mans)
    )
    prods.append(p)

# Создаем 5 пользователей, их корзины и по 2 товара в каждую
for i in range(1, 6):
    user = User.objects.create_user(username=f"user_{i}", password="password123")
    cart = Cart.objects.create(user=user)
    
    # Добавляем 2 случайных товара в корзину
    for _ in range(2):
        item_product = random.choice(prods)
        CartItem.objects.create(cart=cart, product=item_product, quantity=random.randint(1, 3))

print("База данных успешно заполнена!")

