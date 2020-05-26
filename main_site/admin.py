from django.contrib import admin
from .models import Person, LabSession, Request, Question, RequestHandler, tempStoreUserLocationLink, Topic

# access admin page at 127.0.0.1:8000/admin
# user: dev
# password: password

# Register your models here.
admin.site.register(Person)
admin.site.register(LabSession)
admin.site.register(Request)
admin.site.register(Topic)
admin.site.register(Question)
admin.site.register(RequestHandler)
admin.site.register(tempStoreUserLocationLink)
