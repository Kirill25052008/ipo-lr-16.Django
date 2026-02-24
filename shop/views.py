from django.http import HttpResponse

def index(request):
    return HttpResponse("Главная страница. <br> <a href='/about/'>Об авторе</a> <br> <a href='/shop/'>О магазине</a>")

def about(request):
    return HttpResponse("Автор: Темник Кирилл, Студент группы 88ТП")

def shop_info(request):
    return HttpResponse("Тема: Магазин наборов для создания свечей и мыла.")