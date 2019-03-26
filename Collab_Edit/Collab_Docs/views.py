from django.shortcuts import render,redirect
from . import models
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse
from django import forms
from Collab_Docs.forms import LoginForm,CommentForm,ReplyForm
from Collab_Docs.models import Documents, Comments, Users, Reply
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
		user = Users.objects.get(LOGIN_ID = LOGIN_ID)
		try:
			if(request.POST["input_comment"]): #if comment is to be added
				print("In the funtion")
				form = CommentForm(request.POST)
				if form.is_valid():
					input_comment = request.POST.get('input_comment')
					#print(LOGIN_ID)
					#print(input_comment)
					newComment = Comments(userID=user, docID = id, version = version, comment=input_comment)
					newComment.save()
				#return HttpResponseRedirect(reverse('editor',kwargs={'LOGIN_ID':LOGIN_ID, 'id':id, 'version':version}))
		except: 
			pass
		try:
			if(request.POST["input_reply"]):
				print("Im here")
				form = ReplyForm(request.POST)
				if form.is_valid():
					print("Form valid")
					input_reply = request.POST.get('input_reply')

					reply_comment_id = Comments.objects.get(commentID=request.POST.get('reply_com_id'))
						
					reply = Reply(commentID =reply_comment_id, userID= user, reply =input_reply)
					print("SAVEIT")
					reply.save()
				#return HttpResponseRedirect(reverse('editor',kwargs={'LOGIN_ID':LOGIN_ID, 'id':id, 'version':version}))
		except: 
			pass
		try:
			if(request.POST['contents']):
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
		except: 
			pass
		

	# If this is a GET (or any other method) create the default form.
	print("here")
	doc = Documents.objects.filter(docID=id,version=version)
	comment = Comments.objects.filter(docID=id)
	replies = []
	for i in comment:
		reply = Reply.objects.filter(commentID=i.commentID)
		replies.append(reply)
	context = {'document':doc, 'LOGIN_ID': LOGIN_ID, 'comment': comment, 'replies':replies}
	return render(request,'editor_page.html', context=context)



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
