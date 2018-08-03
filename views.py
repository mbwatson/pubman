from django.shortcuts import render
from pubman.models import Publication
from staff.models import Employee
from django.views import View
from .forms import PublicationAddForm, PublicationConfirmForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from pubman.utils import fetchCitation
from crossref.restful import Works
works = Works()

# General Views

def index(request):
    form = PublicationAddForm()
    context = {
        'form': form,        
    }
    return render(request, 'pubman/index.html', context)

# Publication Views

class PublicationListView(View):
    def get(self, request):
        try:
            publications = Publication.objects.all()
        except Publication.DoesNotExist:
            publications = []
        context = {
            'publications': publications, 
        }
        return render(request, 'pubman/publication-list.html', context)

class PublicationListByAuthorView(View):
    def get(self, request, staff_slug):
        try:
            publications = Publication.objects.all()
            publications = publications.filter(author__employee__slug=staff_slug)
            employee = Employee.objects.get(slug=staff_slug)
        except Publication.DoesNotExist:
            publications = []
        except Employee.DoesNotExist:
            employee = None
        context = {
            'employee': employee,
            'publications': publications, 
        }
        return render(request, 'pubman/publication-list.html', context)

class PublicationAddView(View):
    def get(self, request):
        form = PublicationAddForm()
        return render(request, 'pubman/publication-add.html', { 'form': form })

    def post(self, request):
        form = PublicationAddForm(request.POST)
        if form.is_valid():
            doi = request.POST['doi']
            work = works.doi(doi)
            title = work['title'][0]
            citation = fetchCitation(doi)
            publication = {
                'doi': doi,
                'title': title,
                'citation': citation,
            }
            form = PublicationConfirmForm(initial=publication)
            context = {
                'publication': publication,
                'form': form,
            }
            return render(request, 'pubman/publication-confirm.html', context)
        return render(request, 'pubman/publication-add.html', { 'form': form })

class PublicationConfirmView(View):
    def get(self, request):
        context = {}
        return render(request, 'pubman/publication-confirm.html', context)

    def post(self, request):
        publication = Publication()
        form = PublicationConfirmForm(request.POST)
        if form.is_valid():
            publication = form.save()
            form = PublicationAddForm()
            context = {
                'publication': publication,
                'form': form,
            }
            return render(request, 'pubman/publication-thanks.html', context)
        else:
            form = PublicationAddForm()
            return render(request, 'pubman/publication-add.html', { 'form': form })
