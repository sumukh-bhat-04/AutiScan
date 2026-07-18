from django.urls import path
from . import views
from .views import login_view, logout_view, register_view

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', login_view, name='auth'),          # /auth/
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),

    # Password reset (Django built-in views)
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),

    # Custom Admin Dashboard
    path('reset-trigger/', views.trigger_password_reset, name='trigger_password_reset'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('delete-user/<int:user_id>/', views.delete_user_view, name='delete_user'),
    path('reply-feedback/<int:feedback_id>/', views.reply_feedback_view, name='reply_feedback'),
]
