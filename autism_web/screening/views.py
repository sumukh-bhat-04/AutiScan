from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .ml_utils import predict_autism
from .models import ScreeningResult, Feedback


def home(request):
    return render(request, 'home.html')


@login_required(login_url='/auth/')
def predict_view(request):
    context = {}

    if request.method == 'POST':
        age = int(request.POST['age'])
        # gender = int(request.POST['gender']) # Gender not used in current training set
        jaundice = int(request.POST['jaundice'])
        autism_history = int(request.POST['autism_history'])

        # Mapping for 4-point scale
        score_map = {
            "Always": 1.0,
            "Sometimes": 0.6,
            "Rarely": 0.3,
            "Never": 0.0
        }

        # Handle both old logic (binary) and new logic (mapped) just in case, but primary is mapped
        # We assume the form now sends these string values.
        
        aq_scores = []
        for i in range(1, 11):
            val = request.POST.get(f"A{i}")
            if val in score_map:
                aq_scores.append(score_map[val])
            else:
                # Fallback for integer inputs if any
                aq_scores.append(int(val) if val else 0)

        # STRICT ORDER MATCHING TRAIN_V2.PY: ['age', 'jaundice', 'austim', 'A1_Score'...]
        features = [age, jaundice, autism_history] + aq_scores

        prediction, probability = predict_autism(features)
        probability = round(probability * 100, 2)

        if probability >= 70:
            risk = "High"
        elif probability >= 40:
            risk = "Moderate"
        else:
            risk = "Low"

        ScreeningResult.objects.create(
            user=request.user,
            age=age,
            jaundice=jaundice,
            probability=probability,
            risk_level=risk
        )

        context = {
            "risk": risk,
            "probability": probability
        }
        
        return render(request, 'result.html', context)

    return render(request, 'predict.html', context)


@login_required(login_url='/auth/')
def dashboard_view(request):
    results = ScreeningResult.objects.filter(
        user=request.user
    ).order_by('created_at') # Order by date ascending for chart

    # Prepare data for Chart.js
    chart_dates = [result.created_at.strftime("%Y-%m-%d") for result in results]
    chart_probs = [result.probability for result in results]

    # Re-order for list display (newest first)
    results = results.reverse()

    return render(request, 'dashboard.html', {
        'results': results,
        'chart_dates': chart_dates,
        'chart_probs': chart_probs
    })


@login_required(login_url='/auth/')
def history_view(request):
    results = ScreeningResult.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'history.html', {'results': results})


@login_required(login_url='/auth/')
def resources_view(request):
    return render(request, 'resources.html')


@login_required(login_url='/auth/')
def support_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save to Database
        Feedback.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        full_message = f"Message from {name} ({email}):\n\n{message}"

        # Send email to admin
        try:
            send_mail(
                subject=f"Support Request: {subject}",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully! We will contact you shortly.")
        except Exception as e:
            # Even if email fails, we have it in DB now, so maybe show success or warning?
            # Sticking to success behavior as main goal is met.
            messages.success(request, "Your feedback has been recorded.")
        
        return redirect('support')

    return render(request, 'support.html')


from django.contrib import messages

@login_required(login_url='/auth/')
def profile_view(request):
    user = request.user

    # Get age from session (safe, no DB change)
    age = request.session.get('age', '')

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.email = request.POST.get('email')

        # Save age in session
        request.session['age'] = request.POST.get('age')

        user.save()

        messages.success(request, "Profile updated successfully!")

        return redirect('/profile/')

    return render(request, 'profile.html', {
        'user': user,
        'age': age
    })

