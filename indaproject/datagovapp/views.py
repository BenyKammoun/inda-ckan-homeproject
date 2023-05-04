import requests
import json
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.template.loader import render_to_string
from django.shortcuts import render, redirect


DATAGOV_API = 'https://data.gov.il/api/3/action/'


def get_popular_tags():
    url = f"{DATAGOV_API}/package_search?facet.field=[%22tags%22]&facet.limit=10&rows=0"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        # handle error
        return


def get_datasets(request):
    tag = request.GET.get('tag')
    url = f"{DATAGOV_API}/package_search?fq=tags:" + tag
    response = requests.get(url)
    datasets = []
    if response.status_code == 200:
        results = response.json().get('result', {})
        datasets = results.get('results', [])
    return JsonResponse({'datasets': datasets})


def get_dataset_metadata(dataset_id):
    url = f"{DATAGOV_API}/package_show?id={dataset_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        # handle error
        return


def get_dataset_fields(request):
    dataset_id = request.GET.get('dataset_id')
    print(dataset_id)

    metadata = get_dataset_metadata(dataset_id)
    result = metadata.get('result', {})
    resources = result.get('resources', [])
    resource_id = resources[0]["id"]

    url = f"{DATAGOV_API}/datastore_search?resource_id={resource_id}"
    response = requests.get(url)

    if response.status_code == 200:
        fields = response.json()['result']['fields']
        return JsonResponse({'fields': fields})
    return JsonResponse({'error': 'Invalid request'})


def get_query_string(request: HttpRequest):
    if request.method == 'GET':
        selected_fields = ",".join(request.GET.getlist("selected_fields"))
        selected_dataset = request.GET.get("selected_dataset")
        
        print(selected_dataset)
        print(selected_dataset, selected_fields)

        metadata = get_dataset_metadata(selected_dataset)
        result = metadata.get('result', {})
        resources = result.get('resources', [])
        resource_id = resources[0]["id"]

        return HttpResponse(f"{DATAGOV_API}/datastore_search?resource_id={resource_id}&fields={selected_fields}")


def get_dataset_records(request: HttpRequest):
    if request.method == 'POST':
        selected_fields = ",".join(request.POST.getlist("selected_fields"))
        selected_dataset = request.POST.get("selected_dataset")

        metadata = get_dataset_metadata(selected_dataset)
        result = metadata.get('result', {})
        resources = result.get('resources', [])
        resource_id = resources[0]["id"]

        url = f"{DATAGOV_API}/datastore_search?resource_id={resource_id}&fields={selected_fields}"
        response = requests.get(url)
        result = response.json()['result']
        context = {
            'fields': result['fields'],
            'records': result['records']
        }

        print(context['fields'])
        
        html = render_to_string('datagovapp/records.html', context)
        return JsonResponse({"html": html})


def download_dataset(request: HttpRequest):
    selected_fields = ",".join(request.GET.getlist("selected_fields"))
    selected_dataset = request.GET.get("selected_dataset")
    selected_file_format = request.GET.get("file_format")

    return redirect(f"{DATAGOV_API}/datastore_search?resource_id={selected_dataset}&fields={selected_fields}&format={selected_file_format}")


def homeview(request):
    context = {}

    tags = get_popular_tags()
    
    tag_results = tags['result']['facets']['tags']
    context['tag_results'] = tag_results
    
    return render(request, 'datagovapp/index.html', context)
