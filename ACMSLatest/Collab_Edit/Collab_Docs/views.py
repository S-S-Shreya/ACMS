from django.shortcuts import render,redirect
from . import models
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse
from django import forms
from Collab_Docs.forms import LoginForm, CommentForm, ReplyForm, AcceptForm
from Collab_Docs.models import Documents, LatestVersion, Comments, Users, Reply, Accept_Reject, User_Document
import json
import datetime

# Create your views here.

"""
class HomePageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'index.html', context=None)
"""

def DocumentView(request):
	docs = Documents.objects.all().order_by('docname')
	context = {
		'docs_list':docs
	}
	return render(request,'documents.html', context=context)
	
def EditorView(request,LOGIN_ID,id,version,role):
	# If this is a POST request then process the Form data
	user = Users.objects.get(LOGIN_ID = LOGIN_ID)
	if request.method == 'POST':
		
		try:
			if(request.POST['approve']):
				print("hereinapprove")
				docs = Documents.objects.filter(docID=id,version=version).update(approve=True)

		except:
			pass

		try:
			if(request.POST["input_comment"]): 
				#if comment is to be added
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
					bla = Documents.objects.filter(docID=id,version=version).update(lock=0)
					return HttpResponseRedirect(reverse('data',kwargs={'LOGIN_ID':LOGIN_ID}))
					
				else:
					doc = Documents.objects.filter(docID=id)
					trackVersion = 1.0
					for i in doc:
						lastDoc = i
					newVersionNumber = float(lastDoc.version)+1
					newDoc = Documents(docID=lastDoc.docID,docname=lastDoc.docname,version=newVersionNumber,content=x,lock=0) 
					newDoc.save()
					doc = LatestVersion.objects.filter(docVersionID__docID=id).update(latestVersion = newVersionNumber)
					return HttpResponseRedirect(reverse('data',kwargs={'LOGIN_ID':LOGIN_ID}))
				#next = request.POST.get('next', '/')
				#return HttpResponseRedirect(next)
		except: 
			pass
		
		try:
			if(request.POST['accept']):
				form = CommentForm(request.POST)
				x = (request.POST.get('accept'))
				acc_comment_id = Comments.objects.get(commentID=request.POST.get('accepted_cmnt'))
				if(x == '0'):
					vote = Accept_Reject(commentID = acc_comment_id, userID = user, accept = 0, reject = 1)
				else:
					vote = Accept_Reject(commentID = acc_comment_id, userID = user, accept = 1, reject = 0)
				vote.save()

		except:
			pass
		
		try:
			if(request.POST['undo_cmnt']):
				undo_cmnt = (request.POST.get('undo_cmnt'))
				x = Accept_Reject.objects.get(commentID=undo_cmnt, userID= user)
				x.delete()
		except:
			pass

	# If this is a GET (or any other method) create the default form.
	print("here")
	doc = Documents.objects.filter(docID=id,version=version)
	#docObj = Documents.objects.get(docID=id,version=version)
	x = 0
	for x in doc:
		pass
	ReviewerName = None
	if(x.approve == True):
		Reviewer = User_Document.objects.get(docID__docID =id,ROLE="REVIEWER")
		ReviewerName = Reviewer.LOGIN_ID.name
	comment = Comments.objects.filter(docID=id).order_by('-commentID')
	replies = []
	votes = []
	voted_comments = []
	p_voted=[]
	personal_votes=Accept_Reject.objects.filter(userID=user)
	t=Accept_Reject.objects.all().values('commentID')
	temp = personal_votes.values('commentID')
	for pv in temp:
		p_voted.append(pv['commentID'])
	for j in t:
		voted_comments.append(j['commentID'])
	for i in comment:
		reply = Reply.objects.filter(commentID=i.commentID)
		vote = Accept_Reject.objects.filter(commentID=i.commentID)
		replies.append(reply)
		#print("VOTESSS")
		#print(vote)
		votes.append(vote)
		#print(votes)
	flag = 0
	for i in doc:
		flag = i.lock
	if(flag==0):
		bla = Documents.objects.filter(docID=id,version=version).update(lock=1)
		lockingUser = LatestVersion.objects.filter(docVersionID__docID = i.docID).update(lockUser = user)
	latestVersion = LatestVersion.objects.filter(docVersionID__docID = i.docID)
	for x in latestVersion:
		pass
	print(x.lockUser.LOGIN_ID)
	print(LOGIN_ID)
	print("done")
	context = { 'document':doc, 
				'latestVersion' : x.latestVersion, 
				'lockedUser' : x.lockUser.LOGIN_ID,
				'lock':flag, 
				'LOGIN_ID': LOGIN_ID, 
				'comment': comment, 
				'replies':replies, 
				'votes':votes, 
				'personal_votes':personal_votes,
				'personal_v':p_voted,
				'voted_comments':voted_comments,
				'role':role,
				'ReviewerName':ReviewerName }
	return render(request,'editor_page.html', context=context )




def ReadonlyView(request,LOGIN_ID,id,version):
	# If this is a POST request then process the Form data
	if request.method == 'POST':
		print("here1")
		#next = request.POST.get('next', '/')
		#return HttpResponseRedirect(next)
		
	# If this is a GET (or any other method) create the default form.
	else:
		print("here")
		doc = Documents.objects.get(docID=id,version=version)
		latestVersion = LatestVersion.objects.filter(docVersionID__docID = doc.docID)
		for x in latestVersion:
			pass
		print("done")
		context = {'document':doc, 'latestVersion' : x.latestVersion}
		return render(request,'documents.html', context=context)



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
	"""
	else:
		form = LoginForm()
	"""
	return render(request, 'mainpage.html')


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
	return render(request, 'landing.html', context)

def createDoc(request, LOGIN_ID):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:

		#form = LoginForm(request.POST)
		#if form.is_valid():
		print("where are youuuuuu")
		docname = request.POST.get('docname')
		reviewer = request.POST.get('reviewer')
		collaborator = request.POST.get('collaborator')
		print(collaborator)
		try:
			rev = models.Users.objects.filter(pk=reviewer) 
			if rev:
				#for x in collaborator:
				collab = []
				#collab.append(LOGIN_ID)
				i = models.Users.objects.filter(pk=collaborator)
				if i:
					collab.append(i)
							
				else:
					print('\nwrong credentials\n')
					#break
				
				#else:
				doc=Documents(docname=docname,content={})
				doc.save()
				latestttt = LatestVersion(docVersionID=doc, latestVersion=1.0)
				latestttt.save()
				for i in rev:
					print("1")
					addRev = User_Document(LOGIN_ID=i, docID=doc, ROLE = 'REVIEWER' )
					print("2")
					addRev.save()
				for i in collab:
					for j in i:
						print("3")
						addCollab = User_Document(LOGIN_ID=j, docID=doc, ROLE = 'COLLABORATOR' )

						print("4")
						addCollab.save()
					
			else:
				print('\nwrong credentials\n')
			return redirect(reverse('editor', kwargs={'LOGIN_ID':LOGIN_ID, 'id':doc.docID, 'version': 1.0}))
				
		except Exception as e:
			print('\n', e, '\nwrong credentials\n')
	
	return render(request, 'createnew.html')
		
		
