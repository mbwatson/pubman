from django.shortcuts import render
from rest_framework import viewsets, generics
from pubman.models import Publication
from .serializers import PublicationSerializer

class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

    def get_queryset(self):
        queryset = Publication.objects.all()
        doi = self.request.query_params.get('doi', None)
        if doi:
            queryset = queryset.filter(doi=doi)
        return queryset
