from django.contrib import admin
from .models import Creatpost,User,Follower,Likepost

# Register your models here.

admin.site.register(Creatpost)
admin.site.register(User)
admin.site.register(Follower)
admin.site.register(Likepost)