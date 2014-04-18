from django.contrib import admin
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import mail_admins, send_mail
from django.core.exceptions import ValidationError
import random
import string
from datetime import datetime

# http://zmsmith.com/2010/05/django-check-if-a-field-has-changed/
def has_changed(instance, field):
    if not instance.pk:
        return False
    old_value = instance.__class__._default_manager.\
             filter(pk=instance.pk).values(field).get()[field]
    return not getattr(instance, field) == old_value

class Upgrade(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    image = models.ImageField(upload_to='upgrades/', blank=True)
    price = models.IntegerField()

    states = models.ManyToManyField('UpgradeState', help_text='Allowed states')

    def __str__(self):
        return self.title

class AchievementGroup(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()

    def __str__(self):
        return self.title

class RedeemFailure(Exception):
    pass

class Achievement(models.Model):
    title = models.CharField(max_length = 100)
    hint = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='achievements/', blank=True)

    reward = models.IntegerField()
    unlock_key = models.CharField(max_length=12, default=lambda: ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12)))
    group = models.ForeignKey(AchievementGroup)

    parent = models.ForeignKey('self', blank=True, null=True)

    @classmethod
    def key_length(self):
        return Achievement._meta.get_field('unlock_key').max_length

    def __str__(self):
        return self.title

class OrderFailure(Exception):
    pass

class CtfUser(models.Model):
    user = models.OneToOneField(User)
    score = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)

    achievements = models.ManyToManyField(Achievement, through='AchievementLink')
    upgrades = models.ManyToManyField('UpgradeOrder', blank=True)

    def redeem(self, unlock_key):
        try:
            achievement = Achievement.objects.get(unlock_key=unlock_key)
        except Achievement.DoesNotExist:
            raise RedeemFailure('Ungültiger Code.')
        if achievement in self.achievements.all():
            raise RedeemFailure('Code wurde bereits eingelöst.')
        AchievementLink(user=self, achievement=achievement).save()
        self.score += achievement.reward
        self.save()

    def order(self, upgrade):
        if self.score < upgrade.price:
            raise OrderFailure('Sie verfügen nicht über ausreichend Guthaben für diese Bestellung.')
        try:
            order = UpgradeOrder.objects.get(user=self, upgrade=upgrade, state__role='available')
        except UpgradeOrder.DoesNotExist:
            raise OrderFailure('Ungültige Bestellung.')
        order.state = UpgradeState.objects.get(role='ordered')
        self.score -= upgrade.price
        self.save()
        order.save()

    def __str__(self):
        return self.user.username

class AchievementLink(models.Model):
    achievement = models.ForeignKey(Achievement)
    user = models.ForeignKey(CtfUser)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(str(self.user), str(self.achievement))

    def save(self, *args, **kwargs):
        if self.pk is None:
            message = ("Hello,\n"
                       "\n"
                       "user {user} has unlocked the achievement '{achievement}' and received {credit} credit points.\n"
                       "\n"
                       "Best regards\n"
                       "a script").format(user=self.user, achievement=self.achievement.title, credit=self.achievement.reward)
            mail_admins('Achievement unlocked by {user}: {achievement}'.format(user=self.user, achievement=self.achievement), message)
        super().save(*args, **kwargs)

class UpgradeState(models.Model):
    title = models.CharField(max_length = 100)
    subject = models.CharField(max_length = 100, help_text='Email subject')
    message = models.TextField(help_text='Email contents. You can use {upgrade.field} to reference the upgrade.')
    role = models.CharField(max_length=20, blank=True, null=True, help_text='Special role assigned to this state.')

    def __str__(self):
        return self.title

class UpgradeOrder(models.Model):
    upgrade = models.ForeignKey(Upgrade)
    user = models.ForeignKey(CtfUser)
    state = models.ForeignKey(UpgradeState)

    def clean(self):
        try:
            if self.state and self.state not in self.upgrade.states.all():
                valid_states = ', '.join([state.title for state in self.upgrade.states.all()])
                raise ValidationError({'state': ['State not allowed for this upgrade. Valid states: ' + valid_states]})
        except UpgradeState.DoesNotExist:
            pass

    def save(self, *args, **kwargs):
        if self.pk is None or has_changed(self, 'state'):
            message = ("Guten Tag,\n\n" + self.state.message + "\n\nMit freundlichen Grüßen\nAyse Ümeron\n- Leitung {isp} Kundenbetreuung").format(upgrade=self.upgrade, isp=settings.ISP_NAME)
            subject = self.state.subject.format(upgrade=self.upgrade, isp=settings.ISP_NAME)
            send_mail(subject, message, settings.SERVER_EMAIL, [self.user.user.email])
            adm_subject = '[{user}] upgrade {link.upgrade.title} changed state to {link.state}'.format(user=self.user, link=self)
            adm_text = "Hello,\n\nstate of upgrade {link.upgrade.title} changed to {link.state}.\nUser: {user}\n\nBest regards,\na script".format(user=self.user, link=self)
            mail_admins(adm_subject, adm_text)
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(str(self.user), str(self.upgrade))