from django.contrib import admin

from .models import Company, Person, Cache

admin.site.register(Company)
admin.site.register(Person)
admin.site.register(Cache)

