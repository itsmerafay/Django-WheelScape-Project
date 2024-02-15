
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from main import urls as main_app_urls 
from users import urls as users_app_urls
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(main_app_urls)),
    path('', include(users_app_urls)),
]


# static requires actual url for where our files gonna store
# second parameter , where it will point to .

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)