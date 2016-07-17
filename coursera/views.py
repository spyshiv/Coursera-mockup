from django.shortcuts import render
from django.conf import settings
import requests
import json
# Create your views here.
def index(request):
	return render(request, 'index.html', {"static_url": settings.STATIC_URL})

def search(request):
	if request.method == 'POST':
		search_query = request.POST.get('search-query')
		url = "https://api.coursera.org/api/courses.v1?q=search&query="
		fields = "name,partnerIds,partnerLogo" 
		includes = "instructorIds,partnerIds"
		response = requests.get(url + search_query + "&fields=" + fields + "&includes=" + includes).json()
		total = response['paging']['total']
		elements = response['elements']
		return render(request, 'search-result.html', {'total':total, 'elements':elements})
	else:
		return render(request, 'index.html')



	
		