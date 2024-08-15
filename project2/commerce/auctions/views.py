from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import User,Category,Listing,Comment,Biding

def index(request):
    activelisting = Listing.objects.filter(Active=True)
    allcategories = Category.objects.all()

    return render(request, "auctions/index.html", {
        "Category": allcategories,  
        "listings": activelisting
    })       






    


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
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
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password) # type: ignore
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
        Startbid = request.POST["Startbid"]
        Imageurl = request.POST["Imageurl"]
        Active = request.POST["Active"]
        Categorys = request.POST["Categorys"]
        activeuser=request.user

        placedbid = Biding(amount=Startbid, bidder=activeuser)
        placedbid.save()

        SelectedCategoryInstance = Category.objects.get(categoryname = Categorys)

        newlisting = Listing(
            Listingname=Listingname,
            Description=Description,
            Startbid=placedbid,
            Imageurl=Imageurl,
            Active=Active,
            Categorys=SelectedCategoryInstance,    
            Owner=activeuser
        )
        newlisting.save()

        return render(request, "auctions/finishednewlisting.html")
    
def finishednewlisting(request):
    return render(request, "auctions/finishednewlisting.html")

def active_listings(request):
    listings = Listing.objects.filter(Active=True,    )
    return render(request, 'auctions/index.html', {'listings': listings})

    
def learnmore(request, id):
    listinginfo = Listing.objects.get(pk=id)
    userselectlisting = request.user in listinginfo.watchlist.all()
    totalcomments = Comment.objects.filter(listing=listinginfo)
    islistingowner = str(request.user.username) == str(listinginfo.Owner.username)    # type: ignore
    return render(request, "auctions/learnmore.html", {
        "listing": listinginfo,
        "userselectlisting" : userselectlisting,
        "totalcomments" : totalcomments,
        "islistingowner" : islistingowner

})



def endlisting(request, id):
    listinginfo = Listing.objects.get(pk=id)
    listinginfo.Active = False
    listinginfo.save()
    userselectlisting = request.user in listinginfo.watchlist.all()
    totalcomments = Comment.objects.filter(listing=listinginfo)
    islistingowner = str(request.user.username) == str(listinginfo.Owner.username)    # type: ignore
    return render(request, "auctions/learnmore.html", {
        "listing": listinginfo,
        "userselectlisting" : userselectlisting,
        "totalcomments" : totalcomments,
        "islistingowner" : islistingowner

})













def removewatchlist(request, id):
    listinginfo = Listing.objects.get(pk=id)
    activeuser=request.user
    listinginfo.watchlist.remove(activeuser)
    return HttpResponseRedirect(reverse("learnmore",args=(id, )))


def addwatchlist(request, id):
    listinginfo = Listing.objects.get(pk=id)
    activeuser=request.user
    listinginfo.watchlist.add(activeuser)
    return HttpResponseRedirect(reverse("learnmore",args=(id, )))




def watchlist(request):
    activeuser=request.user
    activelisting = activeuser.watchlist.all()
    return render(request, "auctions/watchlist.html",{
        "listings": activelisting

    })



def placeacomment(request, id):
    if request.method == 'POST':
        activeuser = request.user
        listinginfo = Listing.objects.get(pk=id)
        comment = request.POST.get('newcommentsplaced', '')

        newcomment = Comment(
            author=activeuser,
            listing=listinginfo,
            content=comment,
        )
        newcomment.save()  # Make sure to call save() with parentheses

        return HttpResponseRedirect(reverse("learnmore", args=(id,)))
    
    # Handle GET requests or other cases where POST data is not valid
    return HttpResponseRedirect(reverse("learnmore", args=(id,)))




def specificcatagory(request):
    if request.method == "POST":
        categoryFromForm = request.POST['Categorys']
        category=Category.objects.get(  categoryname=categoryFromForm)
        activelisting = Listing.objects.filter(Active=True, Categorys=category,)
        allcategories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "Category": allcategories,  
            "listings": activelisting
        })
    

def placebid(request, id):
    placenewbid = int(request.POST['placenewbid'])
    listinginfo = Listing.objects.get(pk=id)
    if placenewbid > int(listinginfo.Startbid.amount): # type: ignore
        updatetoactivebid = Biding(bidder=request.user, amount=placenewbid)
        updatetoactivebid.save()
        listinginfo.Startbid = updatetoactivebid
        listinginfo.save()
        return render(request, "auctions/bidplacedsuccessfuly.html", {
            "listing":listinginfo
        })
    else:
        return render(request, "auctions/bidplacedunsuccessfuly.html")
