from django.urls import path, include
from . import views
from pubman.views import (
    PublicationListView, PublicationListByAuthorView,
    PublicationAddView, PublicationConfirmView
)
app_name = 'pubman'

urlpatterns = [
    path('', views.index, name='index'),
    path('publications/', PublicationListView.as_view(), name='publication.list'),
    path('publications/add', PublicationAddView.as_view(), name='publication.add'),
    path('publications/confirm', PublicationConfirmView.as_view(), name='publication.confirm'),
    path('publications/<slug:staff_slug>', PublicationListByAuthorView.as_view(), name='publication.list_by_author'),
    path('api/', include('pubman.api.urls')),
]