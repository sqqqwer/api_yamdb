import csv
import glob

from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from yamdb.models import Category, Genre, Review, Title, Comment, TitleGenre

User = get_user_model()


class Command(BaseCommand):
    help = 'Укажите путь к папке с csv документами.'
    model_class_dict = {
        Category.__name__.lower(): Category,
        Genre.__name__.lower(): Genre,
        Review.__name__.lower(): Review,
        Title.__name__.lower(): Title,
        User.__name__.lower(): User,
        Comment.__name__.lower(): Comment,
    }
    many_to_many_class_dict = {
        (Title.__name__.lower(), Genre.__name__.lower()): TitleGenre,
    }

    def add_arguments(self, parser):
        parser.add_argument('path_to_dir', type=str)

    def handle(self, *args, **options):
        csv_list = glob.glob(f'{options["path_to_dir"]}\\*.csv')
        pointer = 0
        if not csv_list:
            raise CommandError('В директории нет .csv файлов')
        while csv_list or pointer > len(csv_list):
            csv_file = csv_list[pointer]
            with open(csv_file, encoding='utf-8-sig') as file:
                file_name = csv_file.split('\\')[-1]
                is_many_to_many, model_key = (
                    self._get_model_key_from_filename(file_name)
                )
                if not model_key:
                    self.stdout.write(
                        f'Файл {file_name} не подходит ни к одной модели.',
                        ending='\n'
                    )
                    csv_list.pop(pointer)
                    continue
                try:
                    if is_many_to_many:
                        model_class = self.many_to_many_class_dict[model_key]
                    else:
                        model_class = self.model_class_dict[model_key]
                    if model_class.objects.all().count() != 0:
                        raise CommandError(
                            (f'Таблица {model_class.__name__} не пуста. '
                             'Удалите и пересоздайте базу данных при помощи '
                             'команды migrate')
                        )
                    self._write_to_database(file, model_class)
                    csv_list.pop(pointer)
                except IntegrityError:
                    csv_list.append(csv_list.pop(pointer))

    def _get_model_key_from_filename(self, file_name):
        for model_name in self.many_to_many_class_dict.keys():
            if '_' in file_name:
                file_name = file_name[:-4].split('_')
                if (
                    model_name[0] in file_name
                    and model_name[1] in file_name
                ):
                    return True, model_name
        for model_name in self.model_class_dict.keys():
            if model_name in file_name:
                return False, model_name
        return None, None

    def _write_to_database(self, file, model_class):
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'id':
                kwarg = {}
                keys = []
                for i in row:
                    if (
                        i in [*self.model_class_dict.keys(), 'author']
                        and '_id' not in i
                    ):
                        i = i + '_id'
                    keys.append(i)
                kwarg = kwarg.fromkeys(keys)
                continue
            for i in range(len(row)):
                kwarg[list(kwarg.keys())[i]] = row[i]
            _, created = model_class.objects.get_or_create(**kwarg)
            self.stdout.write(
                f'Создан экземппляр модели {model_class.__name__}',
                ending='\n'
            )
