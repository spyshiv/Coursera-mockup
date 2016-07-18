from django.shortcuts import render
from django.conf import settings
import requests
import json
from django.template.defaulttags import register
# Create your views here.
def index(request):
	return render(request, 'index.html', {"static_url": settings.STATIC_URL})

def search(request):
	if request.method == 'POST':
		search_query = request.POST.get('search-query')
		return GetData(request, search_query)
	else:
		message = "Please Enter Some strings to search"
		return render(request, 'index.html',{'message':message})

# custom function
def GetData(request, search_query):
	url = "https://api.coursera.org/api/courses.v1?q=search&query="
	fields = "name,partnerIds,instructorIds,partnerLogo" 
	includes = "instructorIds,partnerIds"
	response = requests.get(url + search_query + "&fields=" + fields + "&includes=" + includes).json()
	print url + search_query + "&fields=" + fields + "&includes=" + includes
	total = response['paging']['total']
	page_div = total / 20
	remainder = total % 20
	print "##############", page_div, remainder
	paging = response['paging']
	elements = response['elements']
	partners = response['linked']['partners.v1']
	instructors = response['linked']['instructors.v1']
	return render(request, 'search-result.html', {'search_query':search_query, 'total':total, 'elements':elements, 'partners':partners, 'instructors':instructors })



	
# custom filters
@register.filter(name='filter_partners')
def filter_partners(partners_data, keys):
	result = []
	partners = '';
	for key in keys:
		result = result + filter(lambda item: item['id'] == key, partners_data)
	count = 1
	for partner in result:
		if(count == 1):
			partners = partner['name']
			count += 1
		else:
			partners = partners + ' & ' + partner['name']
	return partners

@register.filter(name='filter_instructors')
def filter_instructors(instructors_data, keys):
	result = []
	instructors = '';
	for key in keys:
		result = result + filter(lambda item: item['id'] == key, instructors_data)
	count = 1
	for instructor in result:
		if(count == 1):
			instructors = instructor['fullName']
			count += 1
		else:
			instructors = instructors + ', ' + instructor['fullName']
	return instructors

	
		