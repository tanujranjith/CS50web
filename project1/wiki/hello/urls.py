from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("tanuj",views.tanuj, name="tanuj" ),
    path("<str:name>", views.greet, name="greet")

]
