import csv
import glob

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model

#from yamdb.models import 


User = get_user_model()

class Command(BaseCommand):
    help = 'Укажите путь к папке с csv документами.'

    def add_arguments(self, parser):
        parser.add_argument('path_to_dir', type=str)

    def handle(self, *args, **options):
        csv_list = glob.glob(f'{options["path_to_dir"]}\\*.csv')
        print(csv_list)
        for csv_file in csv_list:
            csv_file_name = csv_file.split('\\')[-1]
            with open(csv_file) as file:
                reader = csv.reader(file)
                print(csv_file_name)
                print(reader)
