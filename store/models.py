from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
import random
import string

class AchievementGroup(models.Model):
    title = models.CharField(max_length = 100)
    description = models.TextField()

    def __str__(self):
        return self.title

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

    def __str__(self):
        return self.title

class CtfUser(models.Model):
    user = models.OneToOneField(User)
    score = models.IntegerField(default=0)

    achievements = models.ManyToManyField(Achievement, through='AchievementLink')

    def __str__(self):
        return self.user.username

class AchievementLink(models.Model):
    achievement = models.ForeignKey(Achievement)
    user = models.ForeignKey(CtfUser)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(str(self.user), str(self.achievement))
