from django_filters.rest_framework import FilterSet

from documents.models import Document


class DocumentFilterSet(FilterSet):
    class Meta:
        model = Document
        fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'upload_date': ['gte', 'lte'],
        }