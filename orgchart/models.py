from django.db import models

''' Represents a company on the Zenefits platform '''
class Company(models.Model):
	company_id = models.IntegerField(primary_key=True) # Id of the company on Zenefits
	legal_name = models.CharField(max_length=100) # Zenefits API documentation doesn't specify length

	def __str__(self):
		return self.legal_name

''' Represents a person (employee) on the Zenefits platform '''
class Person(models.Model):
	person_id = models.IntegerField(primary_key=True) # Id of the person on Zenefits
	company = models.ForeignKey(Company, on_delete=models.CASCADE) #Every person is an employee of a company
	title = models.CharField(max_length=100, null=True, blank=True) # Zenefits API documentation doesn't specify length
	status = models.CharField(max_length=100, null=True, blank=True) # This could be "active" or null
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	department_name = models.CharField(max_length=100, null=True, blank=True)
	work_location = models.CharField(max_length=100, null=True, blank=True)
	work_email = models.CharField(max_length=100)
	work_phone = models.CharField(max_length=100, null=True, blank=True)
	manager_id = models.IntegerField(null=True, blank=True) # Reference to another "Person" in this table. Can be null if person is at the root of the hierarchy

	def __str__(self):
		return self.first_name+' '+self.last_name

''' Cache. In the form of a Key-Value pair where Key = Token and Value = Company Id '''
class Cache(models.Model):
	token = models.CharField(primary_key=True, max_length=100) # SHA256 encrypted token (length=64)
	company_id = models.IntegerField()
