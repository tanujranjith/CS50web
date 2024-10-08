from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('newlisting', views.newlisting, name='newlisting'),
    path("finishednewlisting", views.finishednewlisting, name="finishednewlisting"),
    path("learnmore/<int:id>", views.learnmore, name="learnmore"),
    path("specificcatagory", views.specificcatagory, name="specificcatagory"), # type: ignore
    path("watchlist", views.watchlist, name="watchlist"),
    path("removewatchlist/<int:id>", views.removewatchlist, name="removewatchlist"),
    path("addwatchlist/<int:id>", views.addwatchlist, name="addwatchlist"),
    path("placeacomment/<int:id>", views.placeacomment, name="placeacomment"),
    path("placebid/<int:id>", views.placebid, name="placebid"),
    path("endlisting/<int:id>", views.endlisting, name="endlisting"),

    
    
]
