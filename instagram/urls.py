from django.contrib import admin
from django.urls import path, include

# Import Static, Media URL
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('photo.urls')), # Photo App URL

    path('', include('django.contrib.auth.urls')), # Include Accounts Templates set
    path('accounts/', include('accounts.urls')),
]

# Media URL
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
