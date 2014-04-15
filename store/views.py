import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from store.models import Achievement, AchievementGroup, AchievementLink, RedeemFailure, UpgradeOrder, UpgradeState, OrderFailure
from store.forms import RedeemForm, OrderForm

# Create your views here.

@login_required
def home(request):
	return render(request, 'store/home.html')

@login_required
def career(request):
	return render(request, 'store/career.html')

@login_required
def contact(request):
	return render(request, 'store/contact.html')

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
	available_all = Achievement.objects.filter(parent__in=achieved)
	available = []
	for a in available_all:
		if a in achieved:
			continue
		available_all.add({'achievement': a, 'unlocks': [a]})
	context = {'groups': groups, 'achieved': achieved, 'available': available, 'form': form}
	return render(request, 'store/achievements.html', context)

@login_required
def upgrades(request):
	context = {'orders': UpgradeOrder.objects.filter(user=request.user.ctfuser)}
	return render(request, 'store/upgrades.html', context)

@login_required
def order_upgrade(request):
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			upgrade = form.cleaned_data['upgrade']
			try:
				request.user.ctfuser.order(upgrade)
				messages.success(request, 'Ihre Bestellung wurde entgegen genommen. Sie werden per E-Mail über den weiteren Verlauf informiert.')
			except OrderFailure as e:
				messages.error(request, str(e))
	return HttpResponseRedirect(reverse('upgrades'))

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
