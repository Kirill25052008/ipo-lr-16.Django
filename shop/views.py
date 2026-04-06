import openpyxl

from io import BytesIO
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Sum, F
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem, Order, OrderItem
from .cart import Cart

def index(request):
    return HttpResponse("Главная страница. <br> <a href='/about/'>Об авторе</a> <br> <a href='/shop/'>О магазине</a>")

def about(request):
    return HttpResponse("Автор: Темник Кирилл, Студент группы 88ТП")

def shop_info(request):
    return HttpResponse("Тема: Магазин наборов для создания свечей и мыла.")

# 1) Список товаров с фильтрацией и поиском
def product_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    manufacturer_id = request.GET.get('manufacturer')
    
    products = Product.objects.all()

    if query:
        # Поиск по названию и описанию через Q-объекты
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    if category_id:
        products = products.filter(category_id=category_id)
        
    if manufacturer_id:
        products = products.filter(manufacturer_id=manufacturer_id)

    return render(request, 'catalog/product_list.html', {'products': products})

# 2) Детальная информация о товаре
def product_detail(request, pk):
    # get_object_or_404 автоматически вернет ошибку 404, если ID не найден
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})

# 3) Добавление товара в корзину
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    cart_item, created = CartItem.objects.get_or_create( # Ищем существующий товар в корзине или создаем новый
        user=request.user, 
        product=product
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    return redirect('cart_view')

# 4) Обновление количества товара
@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    new_quantity = int(request.POST.get('quantity', 1))
    
    
    if new_quantity <= cart_item.product.quantity_in_stock: # Валидация остатка на складе
        cart_item.quantity = new_quantity
        cart_item.save()
    else:
        pass
        
    return redirect('cart_view')

# 5) Удаление товара из корзины
@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')

# 6) Просмотр корзины с подсчетом стоимости
@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    
    
    total_cost = sum(item.product.price * item.quantity for item in cart_items) # Считаем общую стоимость корзины
    
    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total_cost': total_cost
    })

@login_required
def view_cart(request):
    return render(request, 'cart/cart_detail.html')



@login_required
def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        # 1. Создание заказа
        address = request.POST.get('address')
        order = Order.objects.create(user=request.user, address=address)
        
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity']
            )

        # 2. Генерация чека в Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"Order_{order.id}"
        
        headers = ['Товар', 'Цена', 'Количество', 'Сумма']
        ws.append(headers)
        
        for item in cart:
            ws.append([str(item['product']), item['price'], item['quantity'], item['total_price']])
            
        ws.append(['', '', 'ИТОГО:', cart.get_total_price()])

        # Сохраняем в буфер памяти
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        # 3. Отправка чека по Email
        email = EmailMessage(
            f'Ваш заказ №{order.id}',
            'Благодарим за покупку! Чек во вложении.',
            'from@example.com',
            [request.user.email],
        )
        email.attach(f'receipt_{order.id}.xlsx', output.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        email.send()

        # 4. Очистка корзины
        cart.clear()
        return render(request, 'shop/success.html', {'order': order})

    return render(request, 'shop/checkout.html', {'cart': cart})
