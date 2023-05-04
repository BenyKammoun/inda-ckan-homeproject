from django.urls import path
from .views import homeview, get_datasets, get_dataset_fields, get_dataset_records, get_query_string, download_dataset

urlpatterns = [
    path('home/', homeview),
    path('get_datasets/', get_datasets, name="get_datasets"),
    path('get_dataset_fields/', get_dataset_fields, name="get_dataset_fields"),
    path('get_dataset_records/', get_dataset_records, name="get_dataset_records"),
    path('get_query_string/', get_query_string, name="get_query_string"),
    path('download/', download_dataset, name="download")
]
