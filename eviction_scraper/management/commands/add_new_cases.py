from ._private import Eviction_Scraper

from datetime import datetime as dt, timedelta as tdelta

from eviction_scraper.models import EvictionRecord

class Command(Eviction_Scraper):
    help = "scrape new eviction filing records"

    def add_arguments(self, parser):
        # optional argument to add end_date for scraping results
        parser.add_argument('-e', '--end_date', type=str, help='Enter end date to scrape eviction records. Enter as "mmddyyyy"')

    
    def handle(self, *args, **options):
        end_date = options['end_date']
        # get latest filing date from db
        # result is 'datetime.date' type
        last_filed_date = EvictionRecord.objects.latest('filed_date').filed_date    

        start_date = last_filed_date + tdelta(days = 1)

        if end_date is None:
            if (start_date + tdelta(days = 90)) >= dt.today().date():
                end_date = dt.today().date()
            else:
                end_date = start_date + tdelta(days = 90)
            end_date = end_date.strftime("%m%d%Y")
        
        start_date = start_date.strftime("%m%d%Y")
        
        print('start date is ', start_date)
        print('end_date is ', end_date)

        #pd_df = Eviction_Scraper().run_scraper(start_date, end_date)

