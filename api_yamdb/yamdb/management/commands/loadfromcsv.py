import csv
import glob

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from yamdb.models import Category, Genre, Review, Title

User = get_user_model()


class Command(BaseCommand):
    help = 'Укажите путь к папке с csv документами.'
    model_class_dict = {
        Category.__name__.lower(): Category,
        Genre.__name__.lower(): Genre,
        Review.__name__.lower(): Review,
        Title.__name__.lower(): Title,
        User.__name__.lower(): User,
        # Comment.__name__.lower(): Comment,
    }
    many_to_many_class_dict = {
        # TitleGenre.__name__.lower(): TitleGenre,
    }

    def add_arguments(self, parser):
        parser.add_argument('path_to_dir', type=str)

    def handle(self, *args, **options):
        csv_list = glob.glob(f'{options["path_to_dir"]}\\*.csv')
        for csv_file in csv_list:
            with open(csv_file, encoding='utf-8-sig') as file:
                file_name = csv_file.split('\\')[-1]
                print(file_name)
                is_many_to_many, model_key = (
                    self._get_model_key_from_filename(file_name)
                )
                if is_many_to_many:
                    print('МЭНИТУМЭНИ')
                    continue
                    # self._write_to_database(file, model_key)
                if model_key == None:
                    print('НЕТ ТАКОЙ МОДЕЛИ')
                    continue
                print(model_key)
                self._write_to_database(file, self.model_class_dict[model_key])

    def _get_model_key_from_filename(self, file_name):
        if (Genre.__name__ in file_name
            and Title.__name__ in file_name):
            return True, 'jdjd'
        # for model_name in self.many_to_many_class_dict.keys():
            # if model_name in file_name:
                # return TitleGenre.__name__
        for model_name in self.model_class_dict.keys():
            if model_name in file_name:
                return False, model_name
        return None, None

    def _write_to_database(self, file, model_class):
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'id':
                kwarg = {}
                keys = [i for i in row]
                kwarg = kwarg.fromkeys(keys)
                continue
            for i in range(len(row)):
                kwarg[list(kwarg.keys())[i]] = row[i]
            _, created = model_class.objects.get_or_create(**kwarg)
