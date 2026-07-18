from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from screening.models import ScreeningResult

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists") 
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        # login(request, user) # Removed auto-login as per request
        messages.success(request, "Profile created successfully! Please login.")
        return redirect('login')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.username == 'shadow' or user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('/dashboard/')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'auth.html')

def logout_view(request):
    logout(request)
    return redirect('/')

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from screening.models import Feedback

# ... (dashboard logic)

@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard_view(request):
    # Counts
    total_users = User.objects.count()
    total_screenings = ScreeningResult.objects.count()
    total_feedback = Feedback.objects.count()
    
    # Recent activity
    all_screenings = ScreeningResult.objects.order_by('-created_at')
    
    # All Users list
    all_users = User.objects.all().order_by('-date_joined')
    
    # Feedback list
    all_feedbacks = Feedback.objects.all().order_by('-created_at')
    
    # Chart Data
    low_risk = ScreeningResult.objects.filter(risk_level__iexact='Low').count()
    moderate_risk = ScreeningResult.objects.filter(risk_level__iexact='Moderate').count()
    high_risk = ScreeningResult.objects.filter(risk_level__iexact='High').count()
    
    context = {
        'total_users': total_users,
        'total_screenings': total_screenings,
        'total_feedback': total_feedback,
        'recent_screenings': all_screenings,
        'all_users': all_users,
        'all_feedbacks': all_feedbacks,
        'risk_data': [low_risk, moderate_risk, high_risk],
        'high_risk_count': high_risk,
    }
    
    return render(request, 'custom_admin.html', context)

@user_passes_test(lambda u: u.is_superuser)
def delete_user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_superuser: # Prevent deleting other admins comfortably
        user.delete()
        messages.success(request, f"User {user.username} deleted successfully.")
    else:
        messages.error(request, "Cannot delete superuser accounts.")
    return redirect('admin_dashboard')

@user_passes_test(lambda u: u.is_superuser)
def reply_feedback_view(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.method == "POST":
        reply_message = request.POST.get('reply_message')
        try:
            send_mail(
                subject=f"Reply to: {feedback.subject}",
                message=reply_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[feedback.email],
                fail_silently=False,
            )
            feedback.is_replied = True
            feedback.save()
            messages.success(request, f"Reply sent to {feedback.email}")
        except Exception as e:
            messages.error(request, "Failed to send email reply.")
    
    return redirect('admin_dashboard')


from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/auth/login/')
def trigger_password_reset(request):
    """
    Sends a specific password reset email to the currently logged-in user
    without asking them to re-enter their email address.
    """
    if request.method == 'POST':
        user = request.user
        email = user.email
        
        # Initialize standard PasswordResetForm with the user's email
        form = PasswordResetForm({'email': email})
        
        if form.is_valid():
            # The form handles token generation and email sending
            # using the registration/password_reset_email.html template
            form.save(
                request=request, 
                use_https=request.is_secure(),
                from_email=None, 
                email_template_name='registration/password_reset_email.html'
            )
            messages.success(request, f"A password reset link has been sent to {email}")
        else:
            messages.error(request, "Could not send reset email. Please try again.")
            
        return redirect('profile')
    
    # If accessed via GET, just redirect ensuring we don't do accidental sends (though safe-ish)
    return redirect('profile')
