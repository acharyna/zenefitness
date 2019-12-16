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
				new_company = Company(company_id=self.company_id, legal_name=result['data']['name'])
				new_company.save()

				result = self.get_request('https://api.zenefits.com/core/people/?includes=company+manager+department+location', token)
				if result['success'] == True:
					for person in result['data']:
						print(person)

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
