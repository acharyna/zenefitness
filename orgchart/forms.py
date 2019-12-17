from django import forms
from django.conf import settings
from .models import Company, Person, Cache
import requests, hashlib

class ZenefitsForm(forms.Form):
	token = forms.CharField(max_length=32)
	company_id = 0
	is_cached = False

	def fetch_data(self):
		result = {}
#		result['success'] = False
		token = self.cleaned_data['token']
		encrypted_token = hashlib.sha256(token.encode()).hexdigest() # Create a sha256 hash of the token

		try:
			# Check if the encrypted token is present in the cache
			cache = Cache.objects.get(pk=encrypted_token)
			self.company_id = cache.company_id
			company = Company.objects.get(pk=self.company_id)
			self.is_cached = True
			result['success'] = True
		except:
			pass

		# If the token is not available in the cache, then it means we have to fetch all the data from Zenefits
		if not self.is_cached:
			# Fetch Company details for this token using the "Me" Zenefits API
			# Ex: curl -i https://api.zenefits.com/core/me -H "Authorization: Bearer XXXX"
			result = self.get_request('https://api.zenefits.com/core/me', token)
			if result['success'] == True:
				# Using the URI fetched for the company, get the company Id using the Zenefits "Companies" API
				# Ex: curl -i https://api.zenefits.com/core/companies/216397 -H "Authorization: Bearer XXXX"
				result = self.get_request(result['data']['company']['url'], token)
				if result['success'] == True:
					self.company_id = result['data']['id']
	
					# Save this new company to the model/database
					#new_company = Company(company_id=self.company_id, legal_name=result['data']['name'])
					new_company = Company()
					new_company.company_id = self.company_id
					new_company.legal_name = result['data']['name']
					new_company.save()
	
					# Fetch all employees of this company using the Zenefits "People" API
					# Ex: curl -i https://api.zenefits.com/core/people/?includes=company+manager+department+location -H "Authorization: Bearer XXXX"
					result = self.get_request('https://api.zenefits.com/core/people/?includes=company+manager+department+location', token)
					if result['success'] == True:
						for person in result['data']['data']:
							new_person = Person()
							new_person.person_id = person['id']
							new_person.company = new_company
							new_person.status = person['status']
							new_person.title = person['title']
							new_person.first_name = person['first_name']
							new_person.last_name = person['last_name']
							if person['department'] is not None:
								new_person.department_name = person['department']['name']
							else:
								new_person.department_name = None
							if person['location'] is not None:
								new_person.work_location = person['location']['city']
							else:
								new_person.work_location = None
							new_person.work_email = person['work_email']
							new_person.work_phone = person['work_phone']
							if person['manager'] is not None:
								new_person.manager_id = person['manager']['id']
							else:
								new_person.manager_id = None
							new_person.save()

							# We have managed to successfully fetch all data from Zenefits, therefore add this company to the cache
							cache = Cache(encrypted_token, self.company_id)
							cache.save()

		return result

	def get_request(self, url, token):
		res = {}
		headers = {'Authorization': 'Bearer {}'.format(token)} # Ideally the token wouldn't be passed around, and would be stored in an app config
		response = requests.get(url, headers=headers)

		if response.status_code == 200: # Success
			res = response.json()
			res['success'] = True
			res['message'] = 'Success'
		else:
			res['success'] = False
			res['message'] = 'Failed to fetch data from %s for given token' % url	

		return res

	def was_cached(self):
		return self.is_cached

	def get_company_id(self):
		return self.company_id
