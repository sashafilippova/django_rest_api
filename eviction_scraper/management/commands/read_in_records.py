from eviction_scraper.models import EvictionRecord
from django.core.management.base import BaseCommand

import pandas as pd
import numpy as np

class Command(BaseCommand): 
    help = "Read in records from a given csv file into the database"
    
    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='path to csv file containing data')

    def handle(self, *args, **options):
        data_csv_path = options['csv_path']
        df = pd.read_csv(data_csv_path)

        assert len(df) > 0, 'No records were found to add to the database'

        df = df.drop_duplicates()
        df = df.replace({np.nan: None})  

        dict_records = df.to_dict('index')
        lst_with_models = [EvictionRecord(**value) for _, value in dict_records.items()]
        EvictionRecord.objects.bulk_create(lst_with_models)
