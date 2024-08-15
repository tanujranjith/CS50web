from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Category, Listing, Comment, Biding

def index(request):
    activelisting = Listing.objects.filter(Active=True)
    allcategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "Category": allcategories,  
        "listings": activelisting
    })       

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        phone_number = request.POST.get("phone_number", "")
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.phone_number = phone_number
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def newlisting(request):
    if request.method == "GET":
        allcategories = Category.objects.all()
        return render(request, "auctions/newlisting.html", {
            "Category": allcategories
        })
    else:
        Listingname = request.POST["Listingname"]
        Description = request.POST["Description"]
        Startbid = request.POST.get("Startbid", 0)
        Imageurl = request.POST.get("Imageurl", "")
        Active = request.POST.get("Active") == "yes"  # Convert dropdown value to boolean
        activeuser = request.user

        # Ensure Startbid is treated as an integer, default to 0 if not provided
        try:
            Startbid = int(Startbid)
        except ValueError:
            Startbid = 0

        placedbid = Biding(amount=Startbid, bidder=activeuser)
        placedbid.save()

        newlisting = Listing(
            Listingname=Listingname,
            Description=Description,
            Startbid=placedbid,
            Imageurl=Imageurl,
            Active=Active,
            Owner=activeuser
        )
        newlisting.save()

        return HttpResponseRedirect(reverse("finishednewlisting"))

def finishednewlisting(request):
    return render(request, "auctions/finishednewlisting.html")

def active_listings(request):
    listings = Listing.objects.filter(Active=True)
    return render(request, 'auctions/index.html', {'listings': listings})

def learnmore(request, id):
    listinginfo = get_object_or_404(Listing, pk=id)
    userselectlisting = request.user in listinginfo.watchlist.all()
    totalcomments = Comment.objects.filter(listing=listinginfo)
    islistingowner = str(request.user.username) == str(listinginfo.Owner.username)
    return render(request, "auctions/learnmore.html", {
        "listing": listinginfo,
        "userselectlisting": userselectlisting,
        "totalcomments": totalcomments,
        "islistingowner": islistingowner
    })

def endlisting(request, id):
    listinginfo = get_object_or_404(Listing, pk=id)
    listinginfo.Active = False
    listinginfo.save()
    userselectlisting = request.user in listinginfo.watchlist.all()
    totalcomments = Comment.objects.filter(listing=listinginfo)
    islistingowner = str(request.user.username) == str(listinginfo.Owner.username)
    return render(request, "auctions/learnmore.html", {
        "listing": listinginfo,
        "userselectlisting": userselectlisting,
        "totalcomments": totalcomments,
        "islistingowner": islistingowner
    })

def removewatchlist(request, id):
    listinginfo = get_object_or_404(Listing, pk=id)
    activeuser = request.user
    listinginfo.watchlist.remove(activeuser)
    return HttpResponseRedirect(reverse("learnmore", args=(id, )))

def addwatchlist(request, id):
    listinginfo = get_object_or_404(Listing, pk=id)
    activeuser = request.user
    listinginfo.watchlist.add(activeuser)
    return HttpResponseRedirect(reverse("learnmore", args=(id, )))

def watchlist(request):
    activeuser = request.user
    activelisting = activeuser.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": activelisting
    })

def placeacomment(request, id):
    if request.method == 'POST':
        activeuser = request.user
        listinginfo = get_object_or_404(Listing, pk=id)
        comment = request.POST.get('newcommentsplaced', '')

        newcomment = Comment(
            author=activeuser,
            listing=listinginfo,
            content=comment,
        )
        newcomment.save()
        return HttpResponseRedirect(reverse("learnmore", args=(id,)))
    
    return HttpResponseRedirect(reverse("learnmore", args=(id,)))

def specificcatagory(request):
    if request.method == "POST":
        categoryFromForm = request.POST['Categorys']
        category = get_object_or_404(Category, categoryname=categoryFromForm)
        activelisting = Listing.objects.filter(Active=True, Categorys=category)
        allcategories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "Category": allcategories,  
            "listings": activelisting
        })

def placebid(request, id):
    placenewbid = int(request.POST.get('placenewbid', 0))
    listinginfo = get_object_or_404(Listing, pk=id)
    if placenewbid > int(listinginfo.Startbid.amount):
        updatetoactivebid = Biding(bidder=request.user, amount=placenewbid)
        updatetoactivebid.save()
        listinginfo.Startbid = updatetoactivebid
        listinginfo.save()
        return render(request, "auctions/bidplacedsuccessfuly.html", {
            "listing": listinginfo
        })
    else:
        return render(request, "auctions/bidplacedunsuccessfuly.html")



