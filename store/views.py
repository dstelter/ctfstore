from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from store.models import Achievement, AchievementGroup, AchievementLink

# Create your views here.

@login_required
def home(request):
	return render(request, 'store/home.html')

@login_required
def achievements(request):
	groups = AchievementGroup.objects.prefetch_related('achievement_set').all()
	achieved = request.user.ctfuser.achievements.all()
	context = {'groups': groups, 'achieved': achieved}
	return render(request, 'store/achievements.html', context)

@login_required
def upgrades(request):
	pass
