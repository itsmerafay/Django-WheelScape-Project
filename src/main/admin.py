from django.contrib import admin

# Register your models here.

from .models import Listing,LikedListing


class ListingAdmin(admin.ModelAdmin):
    # returning id just for the readonly purposee
    readonly_fields = ('id',)     # not editable 


class LikedListingAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)     # not editable 

admin.site.register(LikedListing, LikedListingAdmin)
admin.site.register(Listing, ListingAdmin)
