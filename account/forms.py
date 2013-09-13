from django import forms
from django.contrib.auth.models import User
from account.models import UserProfile
from django.forms.extras import widgets
from datetime import date


class RegistrationForm(forms.Form):
	first_name = forms.CharField(label=u"FirstName")
	last_name = forms.CharField(label=u"LastName")
	email = forms.EmailField(label=u"E-Mail",max_length=40)
	password = forms.CharField(label=u"Password",
								widget=forms.PasswordInput())
	password_conf = forms.CharField(label=u"Password (Again)",
								widget=forms.PasswordInput())

	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields["first_name"].widget.attrs = {"placeholder": "Firstname"}
		self.fields["last_name"].widget.attrs = {"placeholder": "Lastname"}
		self.fields["email"].widget.attrs = {"placeholder": "E-Mail"}
		self.fields["password"].widget.attrs = {"placeholder": "Password"}
		self.fields["password_conf"].widget.attrs = {"placeholder": "Password (Again)"}

	def clean_password_conf(self):
		if 'password' in self.cleaned_data:
			password = self.cleaned_data['password']
			password_conf= self.cleaned_data['password_conf']
			if password == password_conf:
				return password_conf
		raise forms.ValidationError('Password does not match.')
	
	def clean_email(self):
		email = self.cleaned_data['email']
		try:
			User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		
		raise forms.ValidationError('email is already exist.')

class ProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ['profile_picture','birthday']
	
	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.fields['birthday'].widget = widgets.SelectDateWidget(
			years=range(date.today().year - 50, date.today().year - 15))

class LoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput())