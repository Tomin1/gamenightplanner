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

from invitations.adapters import BaseInvitationsAdapter
from django.contrib import messages
from django.contrib.auth.models import User
from django.dispatch import Signal
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from social_core.exceptions import AuthForbidden, AuthAlreadyAssociated
from social_core.pipeline.partial import partial

user_signed_up = Signal(providing_args=["request", "user"])

class InvitationAdapter(BaseInvitationsAdapter):
    def get_user_signed_up_signal(self):
        return user_signed_up

def is_signup(strategy, request, user=None, **kwargs):
    # FIXME: Is there a better way to detect this?
    signup = strategy.session_get('account_verified_email', False)
    if signup:
        return {'is_signup': True}
    return {'is_signup': False}

def check_verified_email(strategy, is_signup, **kwargs):
    if is_signup:
        account_verified_email = strategy.session_get('account_verified_email',
                                                      None)
        if account_verified_email is None:
            msg = _("Can not sign up without verified email")
            raise AuthForbidden(backend, msg)
        else:
            return {'account_verified_email': account_verified_email}

@partial
def signup(backend, strategy, is_signup=False, is_new=False, **kwargs):
    if is_signup:  # Signup
        if is_new:
            print("signup", 1)
            try:  # Check if already signed up or not
                user = User.objects.get(
                        email=kwargs.get('account_verified_email'))
            except User.DoesNotExist:
                return strategy.redirect(reverse('account:signup-form',
                        args=(kwargs.get('current_partial').token,)))
            else:
                strategy.session_pop('account_verified_email', None)
                return {'user': user}
        else:  # User existed
            print("signup", 2)
            msg = _("This {} account is already registered.".format(
                    backend.name))
            raise AuthAlreadyAssociated(backend, msg)
    else:  # Login
        if is_new:  # User does not exist
            print("signup", 3)
            raise AuthForbidden(backend)
        else:  # All is good, continue
            print("signup", 4)
            return None

def send_user_signed_up(request, user):
    user_signed_up.send(user.__class__, request=request, user=user)
