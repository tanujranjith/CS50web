from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json 
from django.http import JsonResponse
from .models import User,Creatpost,Follower,Likepost


def index(request):
    totalposts = Creatpost.objects.all().order_by("id").reverse()

    paginator = Paginator(totalposts, 4 )
    pagenum = request.GET.get('postindex')
    pagepost = paginator.get_page(pagenum)

    totallikes = Likepost.objects.all()

    wholikedpost = []
    try:
        for Likes in totallikes:
            if Likes.user.id == request.user.id:
                wholikedpost.append(Likes.post.id)
    except:
        wholikedpost = []

    return render(request, "network/index.html",{
        "totalposts" : totalposts,
        "pagepost":pagepost,
        "wholikedpost":wholikedpost
    })
    
    
def createapost(request):
    if request.method == "POST":
        contetofpost = request.POST['postcontent']
        authorofpost = User.objects.get(pk=request.user.id)
        post = Creatpost(postcontent=contetofpost, user=authorofpost)
        post.save()
        return HttpResponseRedirect(reverse(index))

def viewprofile(request, user_id):
    user = User.objects.get(pk=user_id)
    totalposts = Creatpost.objects.filter(user=user).order_by("id").reverse()

    followingnum = Follower.objects.filter(user=user)
    followernum = Follower.objects.filter(userfollowers=user)

    try:
        checkfollowers = followernum.filter(user=User.objects.get(pk=request.user.id))
        if len(checkfollowers) != 0:
            isuserfollowing = True
        else:
            isuserfollowing = False
    except:
        isuserfollowing = False


    paginator = Paginator(totalposts, 4)
    pagenum = request.GET.get('postindex')
    pagepost = paginator.get_page(pagenum)

    return render(request, "network/profile.html",{
        "totalposts" : totalposts,
        "pagepost":pagepost,
        "displayname" : user.username,
        "followingnum":followingnum,
        "followernum":followernum,
        "isuserfollowing":isuserfollowing,
        "activeuser": user

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def unfollowuser(request):
    custfollow = request.POST['custfollow']
    activeuser = User.objects.get(pk=request.user.id)
    custfollowdata = User.objects.get(username = custfollow)
    f = (Follower.objects.filter(user = activeuser, userfollowers=custfollowdata))[0]
    f.delete()
    custid = custfollowdata.id
    return HttpResponseRedirect(reverse(viewprofile, kwargs={'user_id':custid}))


def followuser(request):     
    custfollow = request.POST['custfollow']
    activeuser = User.objects.get(pk=request.user.id)
    custfollowdata = User.objects.get(username = custfollow)
    f = Follower(user = activeuser, userfollowers=custfollowdata)
    f.save()
    custid = custfollowdata.id
    return HttpResponseRedirect(reverse(viewprofile, kwargs={'user_id':custid}))





def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")



def followedusers(request):
    activeuser = User.objects.get(pk=request.user.id)
    peopleuserisfollowing = Follower.objects.filter(user = activeuser)
    activeposts = Creatpost.objects.all().order_by('id').reverse()

    postsoffollowers = []

    for activepost in activeposts:
        for people in peopleuserisfollowing:
            if people.userfollowers == activepost.user:
                postsoffollowers.append(activepost)
    
    paginator = Paginator(postsoffollowers, 4)
    pagenum = request.GET.get('postindex')
    pagepost = paginator.get_page(pagenum)

    return render(request, "network/userbeingfollowed.html",{
        "pagepost":pagepost
    })

def editpage(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        changepost = Creatpost.objects.get(pk=post_id)
        changepost.content = data["content"]
        changepost.save()
        return JsonResponse({"message":"Your Changes Should Be Up To Date","data":data["content"]})

def removelike (request, post_id):
    post = createapost.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Likepost.objects.filter(user=user, post=post)
    like.delete()
    return JsonResponse({"message":"like removed"})

def addlike (request, post_id):
    post = createapost.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    like = Likepost(user=user, post=post)
    like.save()
    return JsonResponse({"message":"like added"})