from django.http import JsonResponse
from django.http import HttpResponse
from .models import EvictionRecord
from .serializers import EvictionSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import csv

def index(request):
    """View function for home page of site."""

    filed_from = EvictionRecord.objects.earliest('filed_date').filed_date
    to = EvictionRecord.objects.latest('filed_date').filed_date
    total_count = EvictionRecord.objects.count()
    last_updated = EvictionRecord.objects.latest('last_updated').last_updated

    context = {
        'from': filed_from,
        'to': to,
        'total_count': total_count,
        'last_updated': last_updated,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context = context)


@login_required
def return_all_records(request):
    """
    Returns all records from the table_name in db.
    """
    eviction_records = EvictionRecord.objects.all()
    serializer = EvictionSerializer(eviction_records, many= True)

    return JsonResponse({"eviction_case_records": serializer.data})


@login_required
def csv_view(request):
    """
    Create the HttpResponse object with the appropriate CSV header.
    """
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="eviction_court_cases.csv"'},
    )
    case_models = EvictionRecord.objects.all()
    writer = csv.writer(response)
    writer.writerow(['case_id', 'court', 'case_caption', 'judge', 'filed_date',
        'case_type', 'amount', 'disposition', 'disposition_date', 'plaintiff_name',
        'plaintiff_address', 'plaintiff_attorney', 'defendant_name', 'defendant_address',
        'defendant_attorney', 'last_updated'])
    cases = case_models.values_list('case_id', 'court', 'case_caption', 'judge', 'filed_date',
        'case_type', 'amount', 'disposition', 'disposition_date', 'plaintiff_name',
        'plaintiff_address', 'plaintiff_attorney', 'defendant_name', 'defendant_address',
        'defendant_attorney', 'last_updated')
    
    for case in cases:
        writer.writerow(case)

    return response

