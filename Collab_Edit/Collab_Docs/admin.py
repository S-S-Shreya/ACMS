from django.contrib import admin

# Register your models here.

from Collab_Docs.models import Users, Documents, User_Document, LatestVersion

admin.site.register(Users)
admin.site.register(Documents)
admin.site.register(User_Document)
admin.site.register(LatestVersion)
