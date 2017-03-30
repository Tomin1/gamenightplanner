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

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

__all__ = ['events', 'AddedInfoModelMixin']

class AddedInfoModelMixin(models.Model):
    class Meta:
        abstract = True

    added = models.DateTimeField(default=now, verbose_name=_("added"))

    added_by = models.ForeignKey(User, related_name='+',
                                 verbose_name=_("added by"))
