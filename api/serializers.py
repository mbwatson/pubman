from rest_framework import serializers
from pubman.models import Publication, Author

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'is_staff')

class PublicationSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)

    class Meta:
        model = Publication
        fields = ('doi', 'title', 'citation', 'authors')
        lookup_field = ('doi')
