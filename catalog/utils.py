import pandas as pd
from tqdm import tqdm
from .models import Book, Genre, Language

def create_books_from_df(df: pd.DataFrame):

    language = Language.objects.get(short_name__exact='EN')
    all_genres_in_df = df['category'].unique()

    for df_genre in all_genres_in_df:
        genre_in_db = Genre.objects.get_or_create(name=df_genre)

    for num, row in df.iterrows():
        title = row['title']
        summary = row['summary']
        isbn = row['isbn']
        cover = row['cover'].replace('../../', '')
        genre = row['category']

        book = Book.objects.create(title=title, summary = summary, isbn=isbn, language=language, online_cover=cover)
        # Create genre as a post-step
        book_genre = Genre.objects.filter(name__exact = genre)
        book.genre.set(book_genre) # Присвоение типов many-to-many напрямую недопустимо

        book.save()