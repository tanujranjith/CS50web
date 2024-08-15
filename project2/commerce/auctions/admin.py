from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User,Listing, Biding, Comment, Category

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Biding)
admin.site.register(Comment)
admin.site.register(Category)




