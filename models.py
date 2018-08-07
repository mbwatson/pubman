from django.db import models
import requests
from crossref.restful import Works
works = Works()
from staff.models import Employee

# Authors

class AuthorManager(models.Manager):
    def create_author(self, name):
        author = self.create(name=name)
        return author

class Author(models.Model):
    name = models.CharField(max_length=127, blank=False, unique=True)
    employee = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    @property
    def is_staff(self):
        return self.employee is not None
    

    objects = AuthorManager()

# Publications

class PublicationManager(models.Manager):
    
    def create_publication(self, doi):
        publication = self.create(doi=doi)
        return publication

class Publication(models.Model):
    doi = models.CharField(max_length=63, blank=False, unique=True)
    title = models.CharField(max_length=255, blank=True)
    authors = models.ManyToManyField(Author, blank=True)
    citation = models.TextField(blank=True, null=False, default='Unavailable')

    def __str__(self):
        return f'{self.title} ({self.doi})'

    def __repr__(self):
        return str(self.doi)

    def _fetch_citation(self, citation_format='apa'):
        url = f'https://search.crossref.org/citation?format={citation_format}&doi={self.doi}'
        citation = requests.get(url)
        citation.encoding = 'utf-8'
        return citation.text or None

    def save(self, *args, **kwargs):
        work = works.doi(doi=self.doi)
        self.title = work['title'][0]
        self.citation = self._fetch_citation()
        super(Publication, self).save(*args, **kwargs)

