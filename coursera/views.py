from django.shortcuts import render
from django.conf import settings

# Create your views here.
def index(request):
	return render(request, 'index.html', {"static_url": settings.STATIC_URL})