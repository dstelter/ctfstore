

# -*- coding: utf-8 -*-

from django import forms
from store.models import Achievement, AchievementLink, Upgrade

class RedeemForm(forms.Form):
	code = forms.CharField(label='Bonus Code', min_length=Achievement.key_length(), max_length=Achievement.key_length())

class OrderForm(forms.Form):
	upgrade = forms.ModelChoiceField(queryset = Upgrade.objects.all())
