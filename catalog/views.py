from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

# Create your views here.
def catalog_main(request):
    """
        Функция отображения для домашней страницы сайта.
    """
    # Генерация "количеств" некоторых главных объектов
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Доступные книги (статус = 'a')
    # SELECT * FROM public.library
    # SELECT count(*) FROM public.library
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # Метод 'all()' применён по умолчанию.

    context = {'num_books':num_books,
               'num_instances':num_instances,
               'num_instances_available':num_instances_available,
               'num_authors':num_authors}
    
    # Отрисовка HTML-шаблона catalog_main_page.html с данными внутри
    # переменной контекста context
    return render(
        request=request,
        template_name='catalog_main_page.html',
        context=context
    )
