"""Collab_Edit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from Collab_Docs.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('Collab_Docs/', include('Collab_Docs.urls')),
]

#Add URL maps to redirect the base URL to our application

urlpatterns += [
	#path('', RedirectView.as_view(url='/Collab_Docs/', permanent=True)),
    path('<LOGIN_ID>',data, name='data')
]

urlpatterns += [
    path('',login, name='login')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
