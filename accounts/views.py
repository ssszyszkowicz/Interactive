from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.http import JsonResponse
import json
from .models import UserProfile

# @login_required
@csrf_exempt
def save_profile(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        markers = data.get('markers')
        if UserProfile.objects.filter(user=request.user, name=name).exists():
            UserProfile.objects.filter(user=request.user, name=name).update(markers=markers)
            return JsonResponse({'status': 'success'})
        UserProfile.objects.create(name=name, user=request.user, markers=markers)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def load_profiles(request):
    if request.method == 'GET':
        profiles = UserProfile.objects.filter(user=request.user).values('id', 'name')
        return JsonResponse({'profiles': list(profiles)}, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def load_profile(request, profile_id):
    if request.method == 'GET':
        try:
            profile = UserProfile.objects.get(id=profile_id, user=request.user)
            return JsonResponse({'profile': {'name': profile.user.username, 'markers': profile.markers}})
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'Profile not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)
