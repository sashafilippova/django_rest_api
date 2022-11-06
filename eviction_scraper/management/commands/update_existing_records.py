from django.db import transaction
from eviction_scraper.models import EvictionRecord
from ._private import Eviction_Scraper

class Command(Eviction_Scraper):
    help = """For records missing disposition in database, 
        check them online again and update disposition if applicable."""
    
    def add_arguments(self, parser):
        parser.add_argument('-l', '--limit', type = int, 
            help = 'number of records to check for disposition. \
                Default is None (check all records with missing disposition)')
        parser.add_argument('-s', '--size', type = int, default = 100,
            help = 'batch size of records to scrape before updating in db')


    def handle(self, *args, **options):
        limit = options['limit']
        batch_size = options['size']
        
        records = EvictionRecord.objects.filter(disposition__isnull = True)[:limit]
        record_batches = list()

        # create a list of lists (batches)
        for i in range(0, len(records), batch_size):
            record_batches.append(records[i:i + batch_size])

        for batch in record_batches:
            with transaction.atomic():
                cases = [i.case_id for i in batch]
                print('cases batch list is: ', cases)

                # scrape records in recs list
                df = self.scrape_cases_by_id(cases)
                df.set_index('case_id', inplace=True)

                # update db using recs objects
                for record in batch: 
                    record.last_updated = df.loc[record.case_id, 'last_updated']

                    print('disposition is: ', df.loc[record.case_id, 'disposition'])

                    if df.loc[record.case_id, 'disposition'] is not None: 
                        record.disposition = df.loc[record.case_id, 'disposition']
                        record.disposition_date = df.loc[record.case_id, 'disposition_date']

                    record.save()




   