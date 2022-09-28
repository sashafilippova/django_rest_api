from eviction_scraper.models import EvictionRecord
from ._private import Eviction_Scraper
from datetime import datetime as dt, timedelta as tdelta
import numpy as np

class Command(Eviction_Scraper):
    help = "Scrape new eviction filing records and save them in database"

    def add_arguments(self, parser):
        parser.add_argument('-s', '--start_date', type = str, help= 'enter start date to scrape eviction records. Enter as "mmddyyyy"')
        parser.add_argument('-e', '--end_date', type=str, help='enter end date to scrape eviction records. Enter as "mmddyyyy"')

    def handle(self, *args, **options):

        start_date = options['start_date']
        end_date = options['end_date']

        if start_date is None:
            # get latest filing date from db; result is 'datetime.date' type
            last_filed_date = EvictionRecord.objects.latest('filed_date').filed_date    
            start_date = last_filed_date + tdelta(days = 1)
        else:
            start_date = dt.strptime(start_date,"%m%d%Y").date()

        if end_date is None:
            if (start_date + tdelta(days = 90)) >= dt.today().date():
                end_date = dt.today().date()
            else:
                end_date = start_date + tdelta(days = 90)
            end_date = end_date.strftime("%m%d%Y")
        
        if not isinstance(start_date, str):
            start_date = start_date.strftime("%m%d%Y")

        # scrape records from the web
        df = self.run_scraper(start_date, end_date)
        print('successfully finised scraping data and converted into clean df')

        assert len(df) > 0, 'No records were found to add to the database'

        df = df.drop_duplicates()
        df = df.replace({np.nan: None})  

        # convert pd into a dict with format {0: {key0: value0, key1: value1}, 1:{....},}
        dict_records = df.to_dict('index')

        # create a list of EvictionRecord model instances where each instance is a record.
        lst_with_models = [EvictionRecord(**value) for _, value in dict_records.items()]

        # add records to the database in bulk 
        EvictionRecord.objects.bulk_create(lst_with_models)
