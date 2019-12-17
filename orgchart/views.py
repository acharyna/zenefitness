from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms
from .models import Company, Person
from .forms import ZenefitsForm
import gviz_api, logging, sys

# Get an instance of a logger
logger = logging.getLogger(__name__)

cached = True

''' 
Main view. URL: /orgchart/

Shows a text input box for the token. On submitting this token via a POST, 
it fetches employee information using Zenefits API and stores it in the database.
The org chart is drawn using the data from the database
'''
def index(request):
	clear_cache()
	companies = Company.objects.all()
	try:
		if 'token' in request.POST:			# Token present in POST data
			form = ZenefitsForm(request.POST)
			if form.is_valid():			# Valid token
				result1 = form.fetch_data()	# Get Zenefits data using token
				if result1['success'] == True:
					company_id = form.get_company_id()
					global cached
					cached = form.was_cached()
				else:
					raise Exception(result1['message'])
			else:
				raise Exception("Error in token")	# Problem with token, print error message
		else:						# Token not present in POST, so render normal index page
			form = ZenefitsForm()
			return render(request, 'orgchart/index.html', {'form':form, 'companies':companies})
	except Exception as error:				# Render index page with error
		return render(request, 'orgchart/index.html', {'form':form, 'companies':companies, 'error_message': "Error: "+repr(error)})
	else:							# Redirect to company details page
		return HttpResponseRedirect(reverse('orgchart:company_detail', args=(company_id,)))

'''
View for a person's details. URL: /orgchart/person/<person_id>/

Shows the details of the person specified by person_id
'''
def person_detail(request, person_id):
	clear_cache()
	person = get_object_or_404(Person, pk=person_id)
	try:
		manager = Person.objects.get(pk=person.manager_id)
	except: # Person.DoesNotExist
		manager = None
	return render(request, 'orgchart/person_detail.html', {'person':person, 'manager':manager})

'''
View for a company's details. URL: /orgchart/company/<company_id>/

Shows the details (eg. Employee Directory) of the company specified by company_id
'''
def company_detail(request, company_id):
	company = get_object_or_404(Company, pk=company_id)
	return render(request, 'orgchart/company_detail.html', {'company':company, 'cached':cached})

'''
View for a company's org chart. URL: /orgchart/company/<company_id>/show/

Shows the org chart of the company specified by company_id
'''
def company_detail_show(request, company_id):
	clear_cache()
	# Prepare a template for the Org Chart page. Note that this is not an usual Django template as it contains Javascript
	# Text substitution is used by Python to create a JS script (Note the %()s). Javascript is needed by the Graphviz library
	# to draw the org chart
	page_template = """
			<html>
			<head>
			<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
			<script type="text/javascript">
				google.charts.load('current', {packages:["orgchart"]});
				google.charts.setOnLoadCallback(drawChart);
				function drawChart() {
							var data = new google.visualization.DataTable(%(json_data_table)s, 0.6);
							var chart = new google.visualization.OrgChart(document.getElementById('chart_div'));
							chart.draw(data, {'allowHtml':true,'allowCollapse':true,'size':'large'});
							}
			</script>
			</head>
			<body>
				<h2>Org Chart for <a href="/orgchart/company/%(company_id)s">%(company)s</a></h2>
				<div id="chart_div"></div>
			</body>
			</html>
			"""
	company = get_object_or_404(Company, pk=company_id)
	company_id = company.company_id

	data_desc = {"node_id": ("string", "Label"), "parent_node": ("string"), "tool_tip": ("string")}
	data_table = gviz_api.DataTable(data_desc)

	#root_employees = company.person_set.all().filter(manager_id__isnull=True)
	chart_data = [{}] # Placeholder to initialise the data structure, will be deleted later
	for employee in company.person_set.all():
		tool_tip = 'Department: {}\nLocation: {}\nEmail: {}\nPhone: {}'.format(employee.department_name, employee.work_location, employee.work_email, employee.work_phone)
		chart_data.append({"node_id": (repr(employee.person_id), str(employee)), "parent_node": employee.manager_id, "tool_tip": tool_tip })

	del chart_data[0] # Remove the placeholder as it messes up the JSON

	data_table.LoadData(chart_data)
	json_data_table = data_table.ToJSon()

	return HttpResponse(page_template % vars())

'''
Delete a given company and redirect to index.html
This also automatically deletes all employees (Person objects) of the company due to the foreign key dependency
'''
def company_delete(request, company_id):
	clear_cache()
	company = get_object_or_404(Company, pk=company_id)
	company_legal_name = company.legal_name
	company.delete()
	return HttpResponseRedirect(reverse('orgchart:index'))

def clear_cache():
	global cached
	cached = True
	return

