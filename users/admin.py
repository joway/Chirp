from django.contrib import admin

# Register your models here.
from .models import User, Oauth

admin.site.register(User)
admin.site.register(Oauth)
