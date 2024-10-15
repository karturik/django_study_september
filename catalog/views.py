from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required
from django.contrib import messages

from django.views import generic
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import datetime
import pandas as pd

from .forms import RenewBookForm, UploadBooksFileForm
from .models import Book, Author, BookInstance, Genre
from .utils import create_books_from_df


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

    paginate_by = 20
    
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='war')[:5] # Получить 5 книг, содержащих 'war' в заголовке

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(BookListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['some_data'] = 'This is just some data'
        return context
    

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list' 
    template_name = 'authors/authors_list_page.html'

    paginate_by = 10


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

    
class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user.
    """
    model = BookInstance
    template_name ='books/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    

class LoanedBooksByAllListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan by all users to librarian.
    """
    model = BookInstance
    template_name ='books/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
    

@permission_required('catalog.can_mark_returned')  
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # Если данный запрос типа POST, тогда
    if request.method == 'POST':

        # Создаём экземпляр формы и заполняем данными из запроса (связывание, binding):
        form = RenewBookForm(request.POST)

        # Проверка валидности данных формы:
        if form.is_valid():
            # Обработка данных из form.cleaned_data
            #(здесь мы просто присваиваем их полю due_back)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # Переход по адресу 'all-borrowed':
            return HttpResponseRedirect(reverse('all-borrowed'))
        
        else:
            print('Form is invalid')
            # Add this else to ensure the invalid form redisplays errors
            return render(request, 'books/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})
        

    # Если это GET (или какой-либо ещё), создать форму по умолчанию.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={
                                    'renewal_date': proposed_renewal_date
                                    })

    return render(request, 'books/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    # initial = {'date_of_death':'12/10/2016',}
    template_name = 'books/book_form.html'
    success_message = "Книга успешно создана."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response
    
class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    template_name = 'books/book_form.html'
    info_message = "Книга успешно изменена."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.info(self.request, self.info_message)
        return response

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books_list')
    template_name = 'books/book_form.html'
    delete_message = "Книга успешно удалена."

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.error(self.request, self.delete_message)
        return response
    

def book_file_upload_view(request):
    if request.method == 'POST':
        if 'file' not in request.FILES:
            return HttpResponse('No file uploaded')
        
        file = request.FILES['file']
        file_format = file.name.split('.')[-1].lower()
        
        if file_format == 'csv':
            try:
                df = pd.read_csv(file)
            except Exception as e:
                return HttpResponse(f'Error reading CSV file: {e}')
        elif file_format in ['xls', 'xlsx']:
            try:
                df = pd.read_excel(file)
            except Exception as e:
                return HttpResponse(f'Error reading Excel file: {e}')
        else:
            return HttpResponse('Unsupported file format')

        create_books_from_df(df)
        
        return HttpResponse(df.to_html())
    else:
        form = UploadBooksFileForm()
        return render(request, 'books/book_file_upload.html', context={'form': form})
