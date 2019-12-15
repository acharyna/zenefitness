from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from .models import Company, Person

''' 
Main view. URL: /orgchart/

Shows a text input box for the token. On submitting this token via a POST, 
it fetches employee information using Zenefits API and stores it in the database.
The org chart is drawn using the data from the database
'''
def index(request):
	'''return render(request, 'orgchart/index.html', {'company': })'''
	return HttpResponse("Enter token:")

'''
View for a person's details. URL: /orgchart/person/<person_id>/

Shows the details of the person specified by person_id
'''
def person_detail(request, person_id):
	person = get_object_or_404(Person, pk=person_id)
	try:
		manager = Person.objects.get(pk=person.manager_id)
	except: # Person.DoesNotExist
		manager = None
	return render(request, 'orgchart/person_detail.html', {'person':person, 'manager':manager})

'''
View for a company's details. URL: /orgchart/company/<company_id>/

Shows the details of the company specified by company_id
'''
def company_detail(request, company_id):
	company = get_object_or_404(Company, pk=company_id)
	return render(request, 'orgchart/company_detail.html', {'company':company})
