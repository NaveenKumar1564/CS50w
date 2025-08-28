from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("Create", views.create_listing, name="create"),
    path("listing/<int:id>",  views.Listing_page, name='Listing'), 
    path("closebid/<int:id>",  views.Close_bid, name='CloseBid'), 
    path("watchlist", views.watchlist, name='watchlist'),
    path("addwatchlist/<int:id>", views.Addwatchlist, name='addwatchlist'),
    path("removewatchlist/<int:id>", views.Removewatchlist, name='removewatchlist'),
    path("Categories", views.Category_Page, name="category"),
    path("Comments", views.Comments, name="Comment"),
    path("AddComments/<int:listing_id>", views.AddComments, name="AddComments"),
    path("categories/<str:category>", views.show_category_listings, name="show"),
    

    
]