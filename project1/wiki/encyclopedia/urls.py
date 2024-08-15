from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="index"),
    path("wiki/new", views.new, name="new"),
    path("wiki/page", views.page, name="page"),
    path("wiki/<str:pagename>", views.greet, name="greet"),
    path("searchwiki", views.searchwiki , name="searchwiki"), # type: ignore
    path("new_page", views.new_page , name="new_page"),
    path("savechangeedit", views.savechangeedit , name="savechangeedit"), # type: ignore
    path("edit", views.edit , name="edit"), # type: ignore
    path("randompage", views.randompage , name="randompage"), # type: ignore


]
