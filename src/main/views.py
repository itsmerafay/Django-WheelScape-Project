from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Listing
from django.contrib import messages
from .forms import ListingForm
from .filters import ListingFilter
from users.forms import LocationForm
from .models import LikedListing
from django.http import JsonResponse

# Create your views here.
def main_view(request):
    return render(request, "views/main.html")

def home_view(request):
    listings = Listing.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=listings)  # because we want to filter through all the objects of Listing                       
    context = {
        # "listings": listings, # as we don't need it anymore as previously we were loading it through all the listing , but now filter listing is needed
        "listing_filter":listing_filter     
    }
    return render(request, "views/home.html", context=context)



@login_required
def list_view(request):
    if request.method == "POST":
        try:
            listing_form = ListingForm(request.POST, request.FILES)
            location_form = LocationForm(request.POST)
            if listing_form.is_valid() and location_form.is_valid():
                listing = listing_form.save(commit=False)
                listing_location = location_form.save()
                listing.seller = request.user.profile
                listing.location = listing_location
                listing.save()
                messages.info(
                    request, f"{listing.model} Listing Posted Successfully"
                )
                return redirect('home')

        except Exception as e:
            print(e)
            messages.error(
                request, "An error occured while posting the listing"
            )

    elif request.method == "GET":
        listing_form = ListingForm()
        location_form = LocationForm()

    return render(request, 'views/list.html', 
                {
                    "listing_form":listing_form,
                    "location_form":location_form
                
                })



@login_required
def listing_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        return render(
            request,
            "views/listing.html",
            {"listing":listing}
        )
    except Exception as e:
        messages.error(request,f"Invalid UUID {id} found was provided for listing")
        return redirect("home")
    
@login_required
def edit_view(request, id):
    try:
        listing = Listing.objects.get(id=id)
        if listing is None:
            raise Exception
        if request.method=="POST":
            listing_form = ListingForm(request.POST, request.FILES, instance=listing)
            location_form = LocationForm(request.POST, request.FILES, instance=listing.location)
            if listing_form.is_valid() and location_form.is_valid():
                listing_form.save()
                location_form.save()
                messages.info(
                    request, f"Listing {id} updated successfully !!"
                )
                return redirect('home')
        else:
            listing_form = ListingForm(instance=listing)
            location_form = LocationForm(instance=listing.location)
            context = {
                "listing_form":listing_form,
                "location_form":location_form
            }

        return render(request, 'views/edit.html', context=context)
        
    except Exception as e:
        messages.error(
            request, f"An error occured while trying to edit the list"
        )
        return redirect('home')


# this view will work for like unlike both 
# liked_listing: It represents the LikedListing object that is either retrieved from the database or created if it doesn't exist.
# created: It is a boolean value that indicates whether the LikedListing object was newly created (True) or already existed (False).

@login_required
def like_listing_view(request, id):
    listing = get_object_or_404(Listing, id=id)
    liked_listing, created = LikedListing.objects.get_or_create(profile=request.user.profile, listing=listing)

    if created: # if it is already existed , so if it is already liked then according to it user is trying to unlike it 
        liked_listing.delete()
    else:
        liked_listing.save()


    return JsonResponse({
        "is_liked_by_user":created # bool
    })