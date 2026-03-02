from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    country = models.CharField(max_length=100, verbose_name="Страна")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    product_image = models.ImageField(upload_to='products/', verbose_name="Фото товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    stock_quantity = models.IntegerField(verbose_name="Количество на складе")
    
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        verbose_name="Категория"
    )
    manufacturer = models.ForeignKey(
        Manufacturer, 
        on_delete=models.CASCADE, 
        verbose_name="Производитель"
    )

    def clean(self):
        if self.price < 0:
            raise ValidationError({'price': "Цена не может быть отрицательной."})
        if self.stock_quantity < 0:
            raise ValidationError({'stock_quantity': "Количество на складе не может быть отрицательным."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Cart(models.Model):
    """Модель корзины, связанная с пользователем."""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Пользователь"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата создания"
    )

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    def total_price(self):
        """Вычисляет общую стоимость всех элементов в корзине."""
        # Используем related_name (по умолчанию cartitem_set) для доступа к элементам
        items = self.cartitem_set.all()
        return sum(item.item_price() for item in items)

class CartItem(models.Model):
    """Модель элемента корзины."""
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        verbose_name="Корзина"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"

    def item_price(self):
        """Возвращает стоимость данного элемента (цена товара * количество)."""
        return self.product.price * self.quantity

    def clean(self):
        """Валидация: количество не должно превышать остаток на складе."""
        if self.quantity > self.product.stock_quantity:
            raise ValidationError(
                f"Недостаточно товара на складе. Доступно: {self.product.stock_quantity}"
            )

    def save(self, *args, **kwargs):
        """Вызов полной валидации перед сохранением."""
        self.full_clean()
        super().save(*args, **kwargs)
