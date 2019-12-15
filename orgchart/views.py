from django.shortcuts import render
from django.http import HttpResponse

''' 
Main view. URL: /orgchart/

Shows a text input box for the token. On submitting this token via a POST, 
it fetches employee information using Zenefits API and stores it in the database.
The org chart is drawn using the data from the database
'''
def index(request):
	return HttpResponse("Enter token: ")

'''
View for a person's details. URL: /orgchart/person/<person_id>/

Shows the details of the person specified by person_id
'''
def person_detail(request, person_id):
	return HttpResponse("You are looking at details of person %s" % person_id)

'''
View for a company's details. URL: /orgchart/company/<company_id>/

Shows the details of the company specified by company_id
'''
def company_detail(request, company_id):
	return HttpResponse("You are looking at details of company %s" % company_id)
