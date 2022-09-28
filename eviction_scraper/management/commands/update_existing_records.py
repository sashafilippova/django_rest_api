from eviction_scraper.models import EvictionRecord
from ._private import Eviction_Scraper

class Command(Eviction_Scraper):
    help = """For records missing disposition in database, 
        check them online again and update disposition if applicable."""
    
    def add_arguments(self, parser):
        parser.add_argument('-l', '--limit', type = int, 
            help = 'number of records to check for disposition. \
                Default is None (check all records with missing disposition)')


    def handle(self, *args, **options):
        limit = options['limit']
        
        print(EvictionRecord.objects.filter(disposition__isnull = True))
        #print(EvictionRecord.objects.all().values_list('disposition', flat=True).distinct())
        records_to_check = None
   