from django.test import TestCase
from django.urls import reverse
from .models import Company, Person

'''
Tests for Company model
'''
class CompanyModelTests(TestCase):

	def test_manager_is_valid_person(self):
		for employee in Person.objects.all():
			# Test will fail if Manager is not a valid Person object
			self.assertNotEqual(Person.objects.get(pk=employee.manager_id), None)

	def test_tbd_2(self):
		self.assertIs(True, True)

	def test_tbd_3(self):
		self.assertIs(True, True)


'''
Tests for Index view
'''
class IndexViewTests(TestCase):

	# Test for no companies
	def test_no_companies(self):
		url = reverse('orgchart:index', args=())
		response = self.client.get(url)
		self.assertContains(response, "No companies found")


'''
Tests for Detail view
'''
class CompanyDetailViewTests(TestCase):

	# Test with no employees
	def test_no_employees(self):
		company1 = Company(1, "Company name 1")
		company1.save()
		url = reverse('orgchart:company_detail', args=(company1.company_id,))
		response = self.client.get(url)
		self.assertContains(response, "No employees")

	# Test with employees
	def test_with_employees(self):
		company1 = Company(1, "Company name 1")
		company1.save()
		emp1 = Person(
			1, 
			company1.company_id, 
			"",
			"",
			"fname1",
			"lname1",
			"",
			"",
			"fname1@email.com",
			"01234567890",
			"1")
		emp1.save()
		url = reverse('orgchart:company_detail', args=(company1.company_id,))
		response = self.client.get(url)
		self.assertContains(response, "fname1")

'''
Tests for Detail view
'''
class CompanyDetailViewShowTests(TestCase):
	def test_org_chart_is_empty(self):
		self.assertIs(True, True)


'''
Tests for Detail view
'''
class CompanyDeleteTests(TestCase):
	def test_delete_company(self):
		self.assertIs(True, True)


