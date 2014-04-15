import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from store.models import Achievement, AchievementGroup, AchievementLink, RedeemFailure
from store.forms import RedeemForm

# Create your views here.

@login_required
def home(request):
	return render(request, 'store/home.html')

@login_required
def achievements(request):
	if request.method == 'POST':
		form = RedeemForm(request.POST)
		if form.is_valid():
			try:
				request.user.ctfuser.redeem(request.POST['code'])
				messages.success(request, 'Bonus erfolgreich eingelöst.')
			except RedeemFailure as e:
				messages.error(request, str(e))
			return HttpResponseRedirect(reverse('achievements'))
	else:
		form = RedeemForm()
	groups = AchievementGroup.objects.prefetch_related('achievement_set').all()
	achieved = request.user.ctfuser.achievements.all()
	context = {'groups': groups, 'achieved': achieved, 'form': form}
	return render(request, 'store/achievements.html', context)

@login_required
def upgrades(request):
	return render(request, 'store/upgrades.html')

def api_redeem(request, user_id, unlock_key):
	try:
		user = User.objects.get(pk=user_id)
		user.ctfuser.redeem(unlock_key)
		response_data = {'success': True, 'message': 'Code erfolgreich eingelöst.'}
	except (RedeemFailure, User.DoesNotExist) as e:
		response_data = {'success': False, 'message': str(e)}
	return HttpResponse(json.dumps(response_data), content_type="application/json")

# Just for testing..
@login_required
def api_has(request, unlock_key):
	try:
		achievement = Achievement.objects.get(unlock_key=unlock_key)
		response_data = {'success': True, 'title': achievement.title, 'description': achievement.description}
	except Achievement.DoesNotExist:
		response_data = {'success': False}
	return HttpResponse(json.dumps(response_data), content_type="application/json")