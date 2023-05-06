import csv

from django.core.management.base import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

model_csv_equal = {
    'static/data/category.csv': Category,
    'static/data/genre.csv': Genre,
    'static/data/titles.csv': Title,
    'static/data/genre_title.csv': GenreTitle,
    'static/data/users.csv': User,
    'static/data/review.csv': Review,
    'static/data/comments.csv': Comment,
}


class Command(BaseCommand):
    """Команда для импорта csv в базу
    Вызов python3 manage.py importcsv
    из терминала в соответствующей папке
    """

    help = 'Импорт csv файлов в таблицы базы'

    def _create_correct_row_fields(self, row):
        """Дополняет строку таблицы экземплярами модели."""
        try:
            if row.get('author'):
                row['author'] = User.objects.get(pk=row['author'])
            if row.get('review_id'):
                row['review'] = Review.objects.get(pk=row['review_id'])
            if row.get('title_id'):
                row['title'] = Title.objects.get(pk=row['title_id'])
            if row.get('category'):
                row['category'] = Category.objects.get(pk=row['category'])
            if row.get('genre'):
                row['genre'] = Genre.objects.get(pk=row['genre'])
        except Exception as error:
            print(f'Ошибка в строке {row.get("id")}.\n'
                  f'Текст - {error}')
        return row

    def handle(self, *args, **options):
        """Тело команды."""
        for i in model_csv_equal.items():
            path, model = i
            rows = 0
            successful = 0
            print(f'Наполняем модель {model.__name__}')
            with open(path, encoding='utf-8', mode='r') as file:
                csv_read = csv.DictReader(file)
                for row in csv_read:
                    rows += 1
                    row = self._create_correct_row_fields(row)
                    try:
                        model.objects.get_or_create(**row)
                        successful += 1
                    except Exception as error:
                        print(f'Ошибка в строке {row.get("id")}.\n'
                              f'Текст - {error}')
            print(f'Наполнение модели {model.__name__} завершено. '
                  f'Строк: {rows}. Успешно: {successful}.',
                  )
