from django.core.management.base import BaseCommand
from eviction_scraper.models import EvictionRecord

# library to export Model records into a pandas data frame
from django_pandas.io import read_frame

class Command(BaseCommand):
    help = "Extracts all records into a csv file"
    
    def add_arguments(self, parser):
        parser.add_argument('csv_path', type = str, 
            help= 'path to csv file where data will be exported') 

    def handle(self, *args, **options):
        csv_path = options['csv_path']
        qs = EvictionRecord.objects.all()
        df = read_frame(qs)

        df.to_csv(csv_path, index= False)