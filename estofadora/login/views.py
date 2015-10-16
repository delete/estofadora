from django.shortcuts import render, redirect
from django.contrib.auth import login as _login

from .forms import LoginForm


def login(request):
	template_name = 'login.html'

	if request.user.is_authenticated():
		return redirect('core:home')

	if request.method == 'POST':
		form = LoginForm(data=request.POST)

		if form.is_valid():
			_login(request, form.get_user())
			return redirect('core:home')
		else:
			return render(request, template_name, {"form": form})
	
	return render(request, template_name, {"form": LoginForm()})