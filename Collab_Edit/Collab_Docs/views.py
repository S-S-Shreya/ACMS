from django.shortcuts import render,redirect
from . import models
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse
from django import forms
from Collab_Docs.forms import LoginForm
from Collab_Docs.models import Documents
import json
import datetime

# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)
        
"""        
class DocumentView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'documents.html', context=None)
"""

def DocumentView(request):
	docs = Documents.objects.all().order_by('docname')
	context = {
		'docs_list':docs
	}
	return render(request,'documents.html', context=context)
	
def EditorView(request,LOGIN_ID,id,version):
	# If this is a POST request then process the Form data
    if request.method == 'POST':
    	print("here1")
    	newVersion = request.POST.getlist('versioning')
    	
    	x=request.POST["contents"]
    	print(x)
    		
    	if(newVersion[0]=="No"):
    		check=Documents.objects.filter(docID=id).update(content=x)
    		print("check:",check)
    		return HttpResponseRedirect(reverse('data',kwargs={'LOGIN_ID':LOGIN_ID}))
    		
    	else:
    		doc = Documents.objects.get(docID=id)
    		newVersionNumber = float(doc.version)+1
    		newDoc = Documents(docID=doc.docID,docname=doc.docname,version=newVersionNumber,content=x,lock=0) #docVersionID=doc.docID
    		newDoc.save()
    		#doc = LatestVersion.objects.get(docID=id).update(latestVersion = newVersionNumber)
    		return HttpResponseRedirect(reverse('data',kwargs={'LOGIN_ID':LOGIN_ID}))
    	#next = request.POST.get('next', '/')
    	#return HttpResponseRedirect(next)
    	
        

    # If this is a GET (or any other method) create the default form.
    else:
    	print("here")
    	doc = Documents.objects.filter(docID=id,version=version)
    	context = {'document':doc}
    	return render(request,'first.html', context=context)



# Create your views here.
def login(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = LoginForm(request.POST)
		if form.is_valid():
			LOGIN_ID = request.POST.get('LOGIN_ID')
			PASSWORD = request.POST.get('PASSWORD')
			
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
	lis=[]
	for i in models.User_Document.objects.filter(LOGIN_ID=LOGIN_ID, ROLE='COLLABORATOR'):
		lis = models.Documents.objects.filter(docID=i.docID.docID)
		#print("LISSSSSSSSSS",lis)
		COLLABORATOR.append(lis)
	for i in models.User_Document.objects.filter(LOGIN_ID=LOGIN_ID, ROLE='REVIEWER'):
		lis = models.Documents.objects.filter(docID=i.docID.docID)
		REVIEWER.append(lis)
	context = {'COLLABORATOR' : COLLABORATOR, 'REVIEWER':REVIEWER, 'LOGIN_ID':LOGIN_ID}
	return render(request, 'index.html', context)
		
		
