from django.shortcuts import redirect, render
import markdown2
from markdown2 import Markdown
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse 
from django import forms
from . import util
from random import choice

class NewPage(forms.Form):
    Title = forms.CharField(label='Title', widget=forms.TextInput)
    Content = forms.CharField(label='Content', widget=forms.Textarea(attrs={'row': 12}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)




def index(request):
    entries= util.list_entries
    return render(request, "encyclopedia/index.html", {
        "entries": entries

    })

def get_page(request, entry):
    m = Markdown()
    EntryPage = util.get_entry(entry)
    if EntryPage is None:
        return render(request, "encyclopedia/error.html", {
            "message": "No page with this entry"    
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": m.convert(EntryPage),
            "Title": entry
        })

def search(request):
    search_req = request.GET.get('q','')
    if(util.get_entry(search_req) is not None):
        return HttpResponseRedirect(reverse("Title", kwargs={'entry': search_req }))
    else:
        Entries = []
        for entry in util.list_entries():
            if search_req.upper() in entry.upper():
                Entries.append(entry)

        return render(request, "encyclopedia/index.html", {
        "entries": Entries,
        "search": True,
        "value": search_req
    })

def New_Page(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data['Title']
            content = form.cleaned_data['Content']
            none = util.get_entry(title) == None or form.cleaned_data['edit'] is True
            if none:
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse('Title', kwargs={'entry': title}))
            else:
                 return render(request, "encyclopedia/NewPage.html", {
                "form": form,
                "Already_Exits": True,
                "entry": title
                })
        else:
            return render(request, "encyclopedia/NewPage.html", {
            "form": form,
            "Already_Exits": False
            })
    else:
        return render(request,"encyclopedia/NewPage.html", {
            "form": NewPage(),
            "Already_Exits": False
        })    

def edit (request, entry):
    EntryPage = util.get_entry(entry)
    if EntryPage is None:
        return render(request, "encyclopedia/error.html",{
            "message": 'No entry with this title'
        })
    else:
        form = NewPage()
        form.fields["Title"].initial = entry     
        form.fields["Title"].widget = forms.HiddenInput()
        form.fields["Content"].initial = EntryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/NewPage.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "Title": form.fields["Title"].initial
        })        

def random_page(request):

    return get_page(request,choice( util.list_entries()))