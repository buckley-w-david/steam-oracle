from django.contrib import admin
from .models import Profile, Game, Game_Entry

admin.site.register(Profile)
admin.site.register(Game)
admin.site.register(Game_Entry)