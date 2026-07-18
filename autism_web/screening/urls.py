from django.urls import path
from .views import (
    home,
    predict_view,
    dashboard_view,
    history_view,
    resources_view,
    support_view,
    profile_view
)

urlpatterns = [
    path('', home, name='home'),
    path('predict/', predict_view, name='predict'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('history/', history_view, name='history'),
    path('resources/', resources_view, name='resources'),
    path('support/', support_view, name='support'),
    path('profile/', profile_view, name='profile'),
]
