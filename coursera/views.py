from django.shortcuts import render
from django.conf import settings
import requests
import json
from django.template.defaulttags import register
# Create your views here.
def index(request):
	return render(request, 'index.html', {"static_url": settings.STATIC_URL})

def search(request):
	if request.method == 'GET':
		search_query = request.GET.get('search-query')
		start = 0
		result_page = 1
		if (request.GET.get('start')):
			start = request.GET.get('start')
		if(request.GET.get('result_page')):
			result_page = request.GET.get('result_page')
		return GetData(request, search_query, str(start), str(result_page))
	else:
		message = "Please Enter Some strings to search"
		return render(request, 'index.html',{'message':message})

# custom function
def GetData(request, search_query, start, result_page):
	url = "https://api.coursera.org/api/courses.v1?q=search&query="
	fields = "name,partnerIds,instructorIds,partnerLogo" 
	includes = "instructorIds,partnerIds"
	response = requests.get(url + search_query + "&fields=" + fields + "&includes=" + includes + "&start=" + start + "&limit=20").json()
	print url + search_query + "&fields=" + fields + "&includes=" + includes
	total = response['paging']['total']
	page_div = Pagination(total)
	print page_div
	paging = response['paging']
	elements = response['elements']
	partners = response['linked']['partners.v1']
	instructors = response['linked']['instructors.v1']
	return render(request, 'search-result.html', {'search_query':search_query, 'total':total, 'elements':elements, 'partners':partners, 'instructors':instructors, 'page_div':range(1,page_div+1), 'result_page':result_page })

def Pagination(total):
	page_no = total / 20
	remain = total % 20
	if remain == 0:
		total_page = page_no
	else:
		total_page = page_no + 1
	return total_page
	

	
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
	
		