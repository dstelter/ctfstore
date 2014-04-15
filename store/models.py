from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import mail_admins
import random
import string

class AchievementGroup(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()

    def __str__(self):
        return self.title

class RedeemFailure(Exception):
    pass

class Achievement(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()
    image = models.ImageField(upload_to='achievements/', blank=True)

    show_title = models.BooleanField(default = True)
    show_description = models.BooleanField(default = True)
    show_image = models.BooleanField(default = True)

    reward = models.IntegerField()
    unlock_key = models.CharField(max_length=12, default=lambda: ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12)))
    group = models.ForeignKey(AchievementGroup)

    @classmethod
    def key_length(self):
        return Achievement._meta.get_field('unlock_key').max_length

    def __str__(self):
        return self.title

class CtfUser(models.Model):
    user = models.OneToOneField(User)
    score = models.IntegerField(default=0)

    achievements = models.ManyToManyField(Achievement, through='AchievementLink')

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
        super(Model, self).save(*args, **kwargs)

