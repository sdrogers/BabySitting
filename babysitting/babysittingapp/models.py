from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Sits(models.Model):
	goingout = models.ForeignKey(User,related_name='goingout',null=True)
	sitting = models.ForeignKey(User,related_name='sitting')
	cost = models.IntegerField(default=1)
	date = models.DateField()

	def __unicode__(self):
		return self.goingout.username

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    balance = models.IntegerField(default=0)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username