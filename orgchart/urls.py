from django.urls import path

from . import views

app_name = 'orgchart'
urlpatterns = [
	# /orgchart/
	path('', views.index, name='index'),
	# /orgchart/person/5/
	path('person/<int:person_id>/', views.person_detail, name='person_detail'),
	# /orgchart/company/3/
	path('company/<int:company_id>/', views.company_detail, name='company_detail'),
	# /orgchart/company/3/show/
	path('company/<int:company_id>/show', views.company_detail_show, name='company_detail_show'),
]

