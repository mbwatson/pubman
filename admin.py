from django.contrib import admin
from pubman.models import Publication, Author

from crossref.restful import Works
works = Works()

#

admin.site.site_header = 'Publications Admin'

#

class AuthorTabularInline(admin.TabularInline):
    model = Author

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee', 'is_staff')
    list_display_links = ('name',)
    list_filter = ('employee',)
    search_fields = ('name',)
    list_editable = ('employee',)
    
    class Meta:
        model = Author

    def is_staff(self, author):
        return author.is_staff

    is_staff.boolean = True
    is_staff.short_description = 'Staff'

admin.site.register(Author, AuthorAdmin)

#

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('doi', 'title')
    exclude = ('authors', 'title', 'citation')
    # inlines = [AuthorTabularInline]

    class Meta:
        model = Publication

    def save_related(self, request, form, formsets, change):
        super(PublicationAdmin, self).save_related(request, form, formsets, change)
        work = works.doi(doi=form.instance.doi)
        form.instance.authors.clear()
        for author in work['author']:
            author_full_name = f'{author.get("given", "")} {author.get("family", "")}'
            if Author.objects.filter(name=author_full_name).exists():
                author = Author.objects.get(name=author_full_name)
            else:
                author = Author.objects.create_author(author_full_name)
            form.instance.authors.add(author)

admin.site.register(Publication, PublicationAdmin)
