from django import urls
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import  *
from django import forms
from django.forms import ModelForm, widgets
from django.contrib.auth.decorators import login_required



class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = [ 'Title', 'Description', 'Category', 'Price', 'Image']
        widgets = {
            'Title': forms.TextInput(attrs={"class": "form-control"}),
            'Description': forms.Textarea(attrs={"class": "form-control"}),
            'Image' : forms.URLInput()
        }
class BidForm(ModelForm):
  class Meta:
    model = Bids
    fields = ["bid"]
    widgets = {
        "bid": forms.IntegerField()
    }


class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = [ "comment"]


Watchings =  []


def index(request):
    if request.method == "POST":
        category = request.POST["category_name"]
        return render(request, "auctions/index.html",{
        'auctions': Listing.objects.filter(Category__in = category[0]).order_by('id')
        })
    else:
          
        return render(request, "auctions/index.html",{
        'auctions': Listing.objects.order_by('id')
          
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
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method== "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():

            #it will save all the inputs

           Title =  form.cleaned_data['Title']
           Description=  form.cleaned_data['Description']
           Category =  form.cleaned_data['Category']
           Price =  form.cleaned_data['Price']
           Image =  form.cleaned_data['Image']
           creator = request.user
           Listing.objects.create(creator = creator, Title = Title, Description = Description, Category = Category, 
            Price = Price, Image = Image)
           return HttpResponseRedirect(reverse(index))
           
        else:
            return render(request, "auctions/Create_Listing.html",{
                'form':form
            })
    else:
        return render(request, "auctions/Create_Listing.html",{
            "form": NewListingForm()
            })



def Listing_page(request, id):
    if request.user.is_authenticated:
        listing = Listing.objects.get(pk =id )               #gives all the information related to the item
        user = User.objects.get(username=request.user)
        if request.method == "POST":
            price = int(request.POST["price"])

            # bids = listing.Current_Bid.all()


            # -----  viewers only (those who don't own) able to bid 
            if user.username != listing.creator.username: 
                if price <= listing.Price:
                    Bid = Bids.objects.order_by('id')
                    return render(request, "auctions/Listing_Page.html", {
                        "Bid":Bid,
                        "listing": listing,
                        "form": BidForm(),
                        "message": "Error! Invalid bid amount!"
                    })
                else:
                    # bid = Bids.objects.create(bid = price , user = user , Auction = listing)
                    current_bids = Bids.objects.filter(Auction=listing)
                    is_zero = current_bids
                    is_highest_bid = 0
                    
                    if(is_zero.count() != 0):
                        for x in current_bids:
                            if x.bid > is_highest_bid:
                                is_highest_bid = x.bid
                        # is_valid_first_bid = price >= listing.Price
                        if is_highest_bid <= price:
                            Bids.objects.create(bid = price , user = request.user , Auction = listing)
                            # current_bids.Auction = listing
                            # current_bids.user = request.user
                            # current_bids.save()
                            listing.buyer = request.user
                            listing.save()
                        else:
                            Bid = Bids.objects.order_by('id')
                            return render(request, "auctions/Listing_Page.html", {
                                "Bid":Bid,
                                "listing": listing,
                                "form": BidForm(),
                                "message": "Error! Invalid bid amount!"
                            })
                    else:
                        Bids.objects.create(bid = price , user = user , Auction = listing)
                        
                
                watchlist = Watchlist.objects.filter(user = request.user, listing = id).count() 
                Bid = Bids.objects.order_by('id')
                return render(request, "auctions/Listing_Page.html",{
                'highest':is_highest_bid,
                'listing': listing,
                'watchlist':watchlist,
                'BidForm': BidForm(),
                'Bid': Bid,
                'Comment': CommentForm(),
                })
                # return HttpResponseRedirect(reverse('Listing', args=(listing.id,)))
               
            else:
                watchlist = Watchlist.objects.filter(user = request.user, listing = id).count()  
                return render(request, "auctions/Listing_Page.html",{
        
                'message':"You can not Bid at your own product",
                'listing': listing,
                'watchlist':watchlist,
                'BidForm': BidForm(),
                # 'Bid': bid,
                'Comment': CommentForm(),
                })
        else:
            watchlist = Watchlist.objects.filter(user = request.user, listing = id).count()
            Bid = Bids.objects.order_by('id')

            return render(request, "auctions/Listing_Page.html",{
            'Bid':Bid,
            'listing': listing,
            'watchlist':watchlist,
            'BidForm': BidForm(),
            'Comment': CommentForm(),
            })



    else:
        listing = Listing.objects.get(pk = id)
        return render(request, "auctions/Listing_Page.html",{

            
            'listing': listing,
        })


def Close_bid(request, id):
    if request.user.is_authenticated:
        listing = Listing.objects.get(pk =id ) #gives all the information related to the item
        user = User.objects.get(username=request.user)
        if request.method == "GET":
            if request.user == listing.creator:
                listing.closed = True
                listing.save()
                watchlist = Watchlist.objects.filter(user = request.user, listing = id).count()
                Bid = Bids.objects.order_by('id')

                return render(request, "auctions/Listing_Page.html",{
                'Bid':Bid,
                'listing': listing,
                'watchlist':watchlist,
                'BidForm': BidForm(),
                'Comment': CommentForm(),
                })



@login_required
def Addwatchlist(request,id):
 
    listId = Listing.objects.get(pk =id )
    creator = request.user
    Watchlist.objects.create(user = creator, listing = listId)
    listing = Listing.objects.get(pk = id)
    watchlist = Watchlist.objects.filter(user = request.user, listing = id).count()
    return render(request, "auctions/Listing_Page.html",{
        'listing': listing,
        'watchlist':watchlist,
    })


@login_required
def Removewatchlist(request,id):
 
    listId = Listing.objects.get(pk =id )
    creator = request.user
    Watchlist.objects.filter(user = creator, listing = listId).delete()
    listing = Listing.objects.get(pk = id)
    watchlist = Watchlist.objects.filter(user = request.user, listing = id).count()
    return render(request, "auctions/Listing_Page.html",{
        'listing': listing,
        'watchlist':watchlist,
    })



@login_required
def watchlist(request):
    
    return render(request, "auctions/Watchlist.html",{
        'watchlist': Watchlist.objects.filter(user = request.user).order_by('id'),
        'auctions': Listing.objects.filter(closed = False).order_by('id')      
    })

def Category_Page(request):

    cat = Categories #gives access of all the categories

    return render(request, "auctions/Categories.html",{

        "Categories": cat

    })


@login_required
def show_category_listings(request, category):
    listings = Listing.objects.filter(Category = category)
    cat = dict(Categories)
    return render(request, 'auctions/specific.html', {
        "listings": listings,
        "category": cat[category]
    })


@login_required
def Comments(request):
    if request.method == "POST":
        form = CommentForm
        if form.is_valid:
            comment = form.save
            HttpResponseRedirect (request, "auctions/Comments.html")

        else:
            return render (request, "auctions/Listing.html")

@login_required
def AddComments(request,listing_id):
    user = User.objects.get(username=request.user)
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.save()
            listing.comments.add(comment)
            listing.save()

            return HttpResponseRedirect(reverse('Listing', args=(listing.id,)))
        else:
            return render(request, "auctions/comment.html", {
                "form": form,
                "listing_id": listing.id,
            })
    else:
        return render(request, "auctions/comment.html", {
            "form": CommentForm(),
            "listing_id": listing.id
        })


