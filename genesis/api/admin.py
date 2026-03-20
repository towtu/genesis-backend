from django.contrib import admin
from api.models import User, Profile, Todo

# Register your models here.

class Useradmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'password']

class Profileadmin(admin.ModelAdmin):
    list_editable =['verified']
    list_display = ['user', 'first_name','last_name', 'bio', 'verified']

class Todoadmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'completed', 'date']

admin.site.register(User, Useradmin)
admin.site.register(Profile, Profileadmin)
admin.site.register(Todo, Todoadmin)

