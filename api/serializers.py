from rest_framework import serializers
from pubman.models import Publication

class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ('doi', 'title', 'citation')
        lookup_field = ('doi')
