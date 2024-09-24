from django.views import generic
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

    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    
    context = {'num_books':num_books,
               'num_instances':num_instances,
               'num_instances_available':num_instances_available,
               'num_authors':num_authors,
               'num_visits': num_visits}
    
    # Отрисовка HTML-шаблона catalog_main_page.html с данными внутри
    # переменной контекста context
    return render(
        request=request,
        template_name='catalog_main_page.html',
        context=context
    )


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'   # ваше собственное имя переменной контекста в шаблоне
    # queryset = Book.objects.filter(title__icontains='war')[:5] # Получение 5 книг, содержащих слово 'war' в заголовке
    template_name = 'books/books_list_page.html'  # Определение имени вашего шаблона и его расположения

    paginate_by = 2
    
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5] # Получить 5 книг, содержащих 'war' в заголовке

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(BookListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['some_data'] = 'This is just some data'
        return context
    

# def book_detail_view(request, pk):
#     try:
#         book_id = Book.objects.get(pk=pk)
#     except Book.DoesNotExist:
#         raise Http404("Book does not exists")

#     #book_id=get_object_or_404(Book, pk=pk)

#     return render(
#         request,
#         'catalog/book_detail.html',
#         context={'book':book_id,}
#     )

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/books_detail_page.html'