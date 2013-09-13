from django.db import models
from django.contrib.auth.models import User
from account.tasks import edit_picture


class UserProfile (models.Model):
	user = models.ForeignKey(User)
	birthday = models.DateField(blank=True, null=True)
	profile_picture = models.ImageField("Profile Picture", upload_to="images/", blank=True, null=True)
	activation_key = models.CharField(max_length=40)
	key_expires = models.DateTimeField()
	is_activated=models.BooleanField(default=False)

	def __unicode__(self):
		return u'%s' % self.user.username
	
	def save(self, *args, **kwargs):
		super(UserProfile, self).save(*args, **kwargs)
		if self.profile_picture:
			edit_picture.delay(self.profile_picture.path)