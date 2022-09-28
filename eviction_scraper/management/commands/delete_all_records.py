from eviction_scraper.models import EvictionRecord
from django.core.management.base import BaseCommand

class Command(BaseCommand): 
    help = "Deletes all records in the database"
    
    def handle(self, *args, **options):
        EvictionRecord.objects.all().delete()
        