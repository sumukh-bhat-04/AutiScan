from django.contrib import admin
from django.urls import path, include
from screening.views import home

urlpatterns = [
    # Home page handled by screening.urls inclusion below


    # Custom auth system
    path('auth/', include('accounts.urls')),

    # Screening app
    path('', include('screening.urls')),

    # Django admin (DO NOT TOUCH)
    path('admin/', admin.site.urls),
]
