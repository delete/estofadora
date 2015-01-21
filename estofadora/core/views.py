from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def home(request):
	return render(request, 'index.html')

def site(request):
	return render(request, 'site.html')