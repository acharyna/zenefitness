from django import forms
from django.conf import settings
from .models import Company, Person
import requests

class ZenefitsForm(forms.Form):
	token = forms.CharField(max_length=32)
	is_cached = False
	company_id = 0

	def fetch_data(self):
		result = {}
#		result['success'] = False
		token = self.cleaned_data['token']

		# Is the token available in the cache?
#		is_cached = (token in request.session[tokens])
#		if not is_cached:

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

#		request.session[tokens] = token # cache the token
#		request.session[tokens][token] = company_id # cache the company_id
#               else:
#                       company_id = request.session[tokens][token]

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

	def clear_cache(self):
#		request.session[tokens].clear()
		return

	def was_cached(self):
		return self.is_cached

	def get_company_id(self):
		return self.company_id
