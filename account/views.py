from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import  get_object_or_404
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from account.tasks import mail_sender
from account.models import UserProfile
from account.forms import RegistrationForm, LoginForm, ProfileForm

from BlogApplication.settings import EMAIL_HOST_USER

import datetime, random, sha

"""Registration view"""
def registration(request, register_success_url="login", template="account/registration.html"):
    form = RegistrationForm()

    if request.POST:
        form = RegistrationForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
        
            user = User.objects.create_user(username=email,
                email=email,
                password=password)

            user.first_name = first_name
            user.last_name = last_name
            user.save()

            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt+user.username).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            user_profile = UserProfile(
            user=user,
            activation_key=activation_key,
            key_expires=key_expires)

            user_profile.save()
            
            current_site = Site.objects.get_current()
            subject = "welcome to my blog"
            message =  ('Please click the link below to'
                'activate your user account \n''%s%s%s') % (
                    current_site, "/account/confirm/", activation_key)

            sender = EMAIL_HOST_USER
            recipients = [email]

            
            mail_sender(subject=subject, message=message,
                        sender=sender, recipients=recipients)

            authenticate(email=email, password=password)


            return redirect(register_success_url)

    return render(request, template, {'form': form})

def confirm(request, activation_key):
    user_profile = get_object_or_404(UserProfile,
                                     activation_key=activation_key)

    if user_profile.key_expires < datetime.datetime.today():
        return redirect(reverse('login'))
    user_account = user_profile.user
    user_account.is_active = True
    user_account.save()
    return redirect(reverse('login'))


""" Login view """
def login_user(request,
               login_success_url="home",
               template="account/login.html"):
    form = LoginForm()

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password) 

            if user is not None:
                login(request, user)
                return redirect(login_success_url)

    ctx={'form': form, 'user':request.user}
    return render(request, template, ctx)


""" Logout view """
@login_required
def logout_user(request, logout_success_url="home"):
    logout(request)
    return redirect(logout_success_url)


def update_profile(request, update_sucess_url="home", template="account/update_profile.html"):
    form = ProfileForm(instance=request.user.get_profile() ,data=request.POST or None)
    if form.is_valid():
        profile_form=form.save(commit=False)
        profile_form.user=request.user
        profile_form.save()
        return redirect(update_sucess_url)

    return render(request, template, {'form':form})