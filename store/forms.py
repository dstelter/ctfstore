from django import forms
from store.models import Achievement, AchievementLink

class RedeemForm(forms.Form):
	code = forms.CharField(label='Bonus Code', min_length=Achievement.key_length(), max_length=Achievement.key_length())
