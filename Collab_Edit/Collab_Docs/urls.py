from django.urls import path
from . import views
from django.conf.urls import url
#from Collab_Docs.views import *

urlpatterns = [
    #url(r'^$', views.HomePageView.as_view()),
    path('documents', views.DocumentView, name='documents'),
    path('documents/<LOGIN_ID>/<id>/<version>', views.EditorView, name='editor'),

]
"""
path('<LOGIN_ID>',data, name='data'),
path('',login, name='login')
"""
