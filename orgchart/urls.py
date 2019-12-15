from django.urls import path

from . import views

urlpatterns = [
	# /orgchart/
	path('', views.index, name='index'),
	# /orgchart/person/5/
	path('person/<int:person_id>/', views.person_detail, name='person_detail'),
	# /orgchart/company/3/
	path('company/<int:company_id>/', views.company_detail, name='company_detail'),
]

