# Copyright (c) 2017, Tomi Leppänen
# This file is part of Game Night Planner
#
# Game Night Planner is free software: you can redistribute it and/or
# modify it under the terms of the Lesser GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Game Night Planner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the Lesser
# GNU General Public License for more details.
#
# You should have received a copy of the Lesser GNU General Public
# License along with Game Night Planner.  If not, see
# <http://www.gnu.org/licenses/>.

from . import AjaxableViewMixin
from ..account import send_user_signed_up
from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError, EmailField
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from social_django.utils import load_strategy

class SignupView(AjaxableViewMixin, TemplateView):
    template_name = 'gamenightplanner/account/signup.html'

class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    email = EmailField(disabled=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        users = User.objects.filter(email=email)
        if users.count() > 0:
            raise ValidationError(_("Email is already registered"))
        if email != self.initial['email']:
            raise ValidationError(_("Email must not be changed"))
        return email

class SignupFormView(AjaxableViewMixin, CreateView):
    template_name = 'gamenightplanner/account/signup_form.html'
    form_class = SignupForm

    def dispatch(self, request, token, *args, **kwargs):
        self.partial = load_strategy().partial_load(token)
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.request.session['account_verified_email']
        return initial

    def get_success_url(self):
        return reverse('social:complete', args=(self.partial.backend,))

    def form_valid(self, form):
        response = super().form_valid(form)
        send_user_signed_up(self.request, self.object)
        return response

class LoginOptionsView(AjaxableViewMixin, TemplateView):
    template_name = 'gamenightplanner/account/login.html'
