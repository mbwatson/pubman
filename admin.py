from django.contrib import admin
from pubman.models import Publication, Author

from crossref.restful import Works
works = Works()

#

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee', 'is_staff')
    
    def is_staff(self, author):
        return author.is_staff

    is_staff.boolean = True
    is_staff.short_description = 'Staff'

admin.site.register(Author, AuthorAdmin)

#

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('doi', 'title')
    exclude = ('author', 'title', 'citation')
    
    def save_related(self, request, form, formsets, change):
        super(PublicationAdmin, self).save_related(request, form, formsets, change)
        work = works.doi(doi=form.instance.doi)
        form.instance.author.clear()
        for author in work['author']:
            ''' Empty strings given as defaults here becuase we don't know if both
            given and family names are provided.'''
            author_full_name = f'{author.get("given", "")} {author.get("family", "")}'
            if Author.objects.filter(name=author_full_name).exists():
                author = Author.objects.get(name=author_full_name)
            else: 
                author = Author.objects.create_author(author_full_name)
            form.instance.author.add(author)

admin.site.register(Publication, PublicationAdmin)