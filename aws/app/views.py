from django.shortcuts import render
from . import models
from django import forms
from app.forms import LoginForm
from django.shortcuts import redirect
from django.urls import reverse

# Create your views here.
def login(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = LoginForm(request.POST)
		if form.is_valid():
			LOGIN_ID = request.POST.get('LOGIN_ID')
			PASSWORD = request.POST.get('LOGIN_ID')
			
			try:
				if models.Users.objects.get(pk=LOGIN_ID).PASSWORD == PASSWORD:
					print(LOGIN_ID+'/data')
					return redirect(reverse('data', kwargs={'LOGIN_ID':LOGIN_ID}))
				else:
					print('\nwrong credentials\n')
					form = LoginForm()
			except Exception as e:
				print('\n', e, '\nwrong credentials\n')
				form = LoginForm()

	else:
		form = LoginForm()

	return render(request, 'LoginUser.html', {'form': form})


def data(request, LOGIN_ID):
	COLLABORATOR, REVIEWER = [], []
	for i in models.User_Document.objects.filter(LOGIN_ID=LOGIN_ID, ROLE='COLLABORATOR'):
		COLLABORATOR.append(i.DOCUMENT_ID)
	for i in models.User_Document.objects.filter(LOGIN_ID=LOGIN_ID, ROLE='REVIEWER'):
		REVIEWER.append(i.DOCUMENT_ID)
	context = {'COLLABORATOR' : COLLABORATOR, 'REVIEWER':REVIEWER}
	return render(request, 'index.html', context)

