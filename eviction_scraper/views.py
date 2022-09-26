from django.http import JsonResponse
from .models import EvictionRecord
from .serializers import EvictionSerializer

def return_all_records(request):
        """
        Returns all records from the table_name in db.
        """
        eviction_records = EvictionRecord.objects.all()
        serializer = EvictionSerializer(eviction_records, many= True)
        return JsonResponse({"eviction_cases": serializer.data})

def scrape_new_records():
    pass
