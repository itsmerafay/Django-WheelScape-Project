
# sender refers to from the model (user profile) -- to invoke this function\
# instance is UserProfile instance (row in our db for each user and each of those )   -- it triggered signal
# created is a boolean value indicating whether a new instance of the model was created or if it's an existing one being saved
# If created is True, it means that a new instance was created.
# receiver expects two things one is signal at which it is going to act (any 4 types of signal according to the condition) and sender from which the signal is coming (User)

# In conclusion, if the user gets saved in the database (post_save , after saving in the database)
# Now we have to register our signal.py to make it recognize


from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Profile, Location

# On the creation of user instance , create the object for Profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# On Profile creation, the location instance will be created
@receiver(post_save, sender=Profile)
def create_profile_location(sender, instance, created, **kwrags):
    if created:
        profile_location = Location.objects.create()
        instance.location = profile_location
        instance.save()


# Deleting Profile will delete the location
# After deleting user profile it will check if it's instance is still present then delete the instance location
@receiver(post_delete, sender=Profile)
def delete_profile_location(sender, instance, **kwargs):
    if instance.location:
        instance.location.delete()

