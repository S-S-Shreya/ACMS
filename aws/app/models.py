from django.db import models
import django

# Create your models here.
class Users(models.Model):
	"""docstring for Users"""
	LOGIN_ID = models.CharField(max_length=50, primary_key=True)
	PASSWORD = models.CharField(max_length=50)
	NAME = models.CharField(max_length=50)
	INSTITUTION = models.CharField(max_length=50, choices=[('COLLEGE', 'C'), ('INSTITUTION', 'I')], default='COLLEGE')
	PROFESSION = models.CharField(max_length=50, choices=[('STUDENT', 'S'), ('PROFESSOR', 'P')], default='STUDENT')

class Documents(models.Model):
	"""docstring for Documents"""
	DOCUMENT_ID = models.CharField(max_length=50, primary_key=True)
	DOCUMENT_NAME = models.CharField(max_length=50)
	VERSION_NUMBER = models.CharField(max_length=50)
	PATH_TO_DOCUMENT = models.CharField(max_length=50)
	LOCK = models.IntegerField(choices=[(0, '0'), (1, '1')], default=1)
class User_Document(models.Model):
	"""docstring for User_Document"""
	LOGIN_ID = models.ForeignKey(Users, on_delete=models.CASCADE)
	DOCUMENT_ID = models.ForeignKey(Documents, on_delete=models.CASCADE)
	ROLE = models.CharField(max_length=50, choices=[('COLLABORATOR', 'C'), ('REVIEWER', 'R')], default='REVIEWER')

	class Meta:
		unique_together = (("DOCUMENT_ID", "LOGIN_ID"),)

class Latest_Version(models.Model):
	"""docstring for Latest_Version"""
	DOCUMENT_ID = models.CharField(max_length=50, primary_key=True)
	LATEST_VERSION = models.DateTimeField(default=django.utils.timezone.now)