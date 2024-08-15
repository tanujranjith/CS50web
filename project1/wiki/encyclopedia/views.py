import random
from django.shortcuts import render
import markdown
from markdown2 import Markdown
markdowner = Markdown()

from . import util

def mdtohtml(title):
    pagecont = util.get_entry(title)
    markdowner = markdown.markdown("title")
    if pagecont == None:
        return None
    else:
        return markdown.markdown(pagecont)


def index(request):
    return render(request, "encyclopedia/index.html", 
    {
        "entries": util.list_entries()
    })

def new(request):
    return render(request, "encyclopedia/new.html",     
    {
        "entries": util.list_entries()
    })

def page(request):
    return render(request, "encyclopedia/page.html", 
    {
        "entries": util.list_entries()
    })

def greet(request, pagename):
    html_content = mdtohtml (pagename)
    if html_content == None:
        return render(request, "encyclopedia/errorpage.html")
    else:
        return render(request, "encyclopedia/page.html",   
        {
            "pagetitle":pagename,
            "pagecontent":html_content
        })
    




def edit(request):
    if request.method == 'POST':
        pagename = request.POST['pagetitle']
        html_content = util.get_entry(pagename)
        return render(request, "encyclopedia/editpage.html",   
        {
            "pagename":pagename,
            "pagecontent":html_content
        })
    
def savechangeedit(request):
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        util.save_entry(title,content)
        html_content= mdtohtml(title)
        return render(request, "encyclopedia/page.html", 
            {
                "pagetitle":title,
                "pagecontent":html_content
            })
    


 
def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/newpagecreatefail.html")
        else:
            util.save_entry(title,content)
            html_content= mdtohtml(title)
            return render(request, "encyclopedia/page.html", 
            {
                "pagetitle":title,
                "pagecontent":html_content
            })
  



        
def searchwiki(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = mdtohtml (entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/page.html",   
            {
                "pagetitle":entry_search,
                "pagecontent":html_content
            })
        else:
            entries = util.list_entries()
            attemptedpage = []
            for entry in entries:
                if entry_search.lower() in entry.lower():
                    attemptedpage.append(entry)
                    return render(request, "encyclopedia/searchbar.html",   
                    {
                        "attemptedpage": attemptedpage
                    })
                else:
                    print("hi")
            


def randompage(request):
    entries=util.list_entries()
    randpage = random.choice(entries)
    return render(request, "encyclopedia/page.html",   
    {
        "pagetitle":randpage,
        "pagecontent":mdtohtml(randpage)
    })

    


            
            
