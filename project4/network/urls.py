
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createapost", views.createapost, name="createapost"),
    path("profile/<int:user_id>", views.viewprofile, name="viewprofile"),
    path("unfollowuser", views.unfollowuser, name="unfollowuser"),
    path("followuser", views.followuser, name="followuser"),
    path("profile/followedusers", views.followedusers, name="profileFollowedusers"),
    path("followedusers", views.followedusers, name="followedusers"),
    path("editpage/<int:post_id>", views.editpage, name="editPage"),
    path("removelike/<int:post_id>", views.removelike, name="removelike"),
    path("addlike/<int:post_id>", views.addlike, name="addlike"),




]
