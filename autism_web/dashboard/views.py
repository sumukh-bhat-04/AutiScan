from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from screening.models import ScreeningResult

@login_required(login_url='/auth/')
def dashboard_view(request):
    results = ScreeningResult.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'dashboard.html', {
        'results': results
    })
