# Instance and filename will be provided
# The .format is for string formatting, here the curly braces will correspond to what is provided in the .format
# Here we've created a custom folder for the storage of user's images 
# It will saved in the format , user followed by user.id and name of the file 
def user_directory_path(instance, filename):
    return "user_{0}/{1}".format(instance.user.id, filename)