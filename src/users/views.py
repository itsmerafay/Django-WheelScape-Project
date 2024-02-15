from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from main.models import Listing, LikedListing
from django.utils.decorators import method_decorator
from .forms import UserForm, ProfileForm, LocationForm

def login_view(request):

    if request.method == "POST":
        login_form = AuthenticationForm(request=    request, data = request.POST) ## thixs login_form caries django form which is then applied to the templatig
        if login_form.is_valid():
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")
            user = authenticate(request=request, username = username, password = password)
            print(user)
            if user is not None :
                login(request, user)
                messages.success(request, f"Successfully logged in as {username}.")
                return redirect("home")  # we set nothing here we defined the login settings in settings.py # a powerful django tool that will directly gonna redirect due to our defined settings 
        else:
            messages.error(request, f"An error occured while trying to login !")

    elif request.method == "GET": # for get just return the auth form 
        login_form = AuthenticationForm()

    return render(request, "views/login.html", {"login_form":login_form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


class RegisterView(View):
# Will handle the get request 
    def get(self, request):
        register_form = UserCreationForm()
        return render(request, "views/register.html", {
            "register_form":register_form
        })
    
    def post(self, request):
        register_form = UserCreationForm(data = request.POST)
        if register_form.is_valid():
            user = register_form.save()
            # user.refresh_from_db()  # This refresh method is particularly useful when you want to update an instance with the latest data from the database
            # login(request, user)
            messages.success(
                request, f"{user.username} registered successfully!"
            )
            return redirect("login")  
        else:
            messages.error(
                request, f"Register Unsuccessful !"
            )
            return render(request, "views/register.html", {
                "register_form":register_form
            })
        

# Routing Requests: When a request is made to a view class, Django calls the dispatch method first. This method examines the HTTP method of the request and routes it to the corresponding method in the view class (get, post, etc.).
# View class has dispatch method , it is called whenever a request is made.

@method_decorator(login_required, name="dispatch")
class ProfileView(View):


    def get(self, request):
        user_listing = Listing.objects.filter(seller=request.user.profile)
        user_liked_listing = LikedListing.objects.filter(profile=request.user.profile).all()
        user_form = UserForm(instance=request.user) # will give the 3 values from the user table currently
        profile_form = ProfileForm(instance=request.user.profile)
        location_form = LocationForm(instance=request.user.profile.location)

        context = {
            "user_form":user_form,  
            "profile_form":profile_form,
            "location_form":location_form,
            "user_listing":user_listing,
            "user_liked_listing":user_liked_listing
        }
        print(user_liked_listing)
        
        return render(request, "views/profile.html",context=context)


    def post(self, request):
        user_listing = Listing.objects.filter(seller=request.user.profile)
        user_liked_listing = LikedListing.objects.filter(profile=request.user.profile).all()
        user_form = UserForm(request.POST, instance=request.user) # will give the 3 values from the user table currently
        profile_form = ProfileForm(request.POST,request.FILES,instance=request.user.profile) 
        location_form = LocationForm(request.POST, instance=request.user.profile.location)


        if user_form.is_valid() and location_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            location_form.save()
            messages.info(request, "Profile Updated Successfully !!")

        else:
            messages.error(
                request, "Error in saving the profile updates"
            )

        context = {
            "user_form":user_form,
            "profile_form":profile_form,
            "location_form":location_form,
            "user_listing":user_listing,
            "user_liked_listing":user_liked_listing
        }

        return render(request, "views/profile.html",context=context)
