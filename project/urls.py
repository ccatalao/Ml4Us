from django.conf.urls import url
from . import views

#app_name = 'project'

urlpatterns = [
    url(r'^$',views.ProjectListView.as_view(),name='project_list'),
    url(r'^project/(?P<pk>\d+)/example/$', views.ProjectExampleView.as_view(), name='project_example'),
    url(r'^project/(?P<pk>\d+)$', views.ProjectDetailView.as_view(), name='project_detail'),
    url(r'^project/new/$',  views.ProjectCreateView.as_view(), name='project_new'),
    url(r'^project/(?P<pk>\d+)/edit/$', views.ProjectUpdateView.as_view(), name='project_edit'),
    url(r'^project/(?P<pk>\d+)/remove/$', views.ProjectDeleteView.as_view(), name='project_remove'),
    # label urls
    url(r'^project/(?P<pk>\d+)/label/$', views.add_label_to_project, name='add_label_to_project'),
    url(r'^label/(?P<pk>\d+)/remove/$', views.label_remove, name='label_remove'),
    url(r'^label/(?P<pk>\d+)/edit/$', views.label_edit, name='label_edit'),
    url(r'^label/(?P<pk>\d+)/import_data/$', views.import_data, name='label_import_data'),
    # docs urls
    url(r'^doc/(?P<pk>\d+)/new/$', views.add_doc_to_label, name='add_doc_to_label'),
    url(r'^doc/(?P<pk>\d+)/remove/$', views.doc_remove, name='doc_remove'),
    url(r'^doc/(?P<pk>\d+)/edit/$', views.doc_edit, name='doc_edit'),
    url(r'^doc/(?P<pk>\d+)/list/$', views.docs_list, name='label_docs_list'),
    #url(r'^doc/(?P<pk>\d+)/list/$',views.DocListView.as_view(),name='doc_list'), 
    #url(r'^project/populate/$',views.PopulateDataView.as_view(),name='populate'),

]