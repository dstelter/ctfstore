from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from store.models import Achievement, AchievementGroup, AchievementLink

# Create your views here.

@login_required
def home(request):
    groups = AchievementGroup.objects.prefetch_related('achievement_set').all()
    #achieved = [l.achievement for l in AchievementLink.objects.filter(user=request.user)]
    achieved = request.user.ctfuser.achievements.all()
    context = {'groups': groups, 'achieved': achieved}
    return render(request, 'store/home.html', context)