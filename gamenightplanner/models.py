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
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from isoweek import Week

class AddedInfoModelMixin(models.Model):
    class Meta:
        abstract = True

    added = models.DateTimeField(default=now, verbose_name=_("added"))

    added_by = models.ForeignKey(User, related_name='+',
                                 verbose_name=_("added by"))

class Event(AddedInfoModelMixin, models.Model):
    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering = ('date', )

    date = models.DateTimeField(verbose_name=_("date"))

    length = models.DurationField(verbose_name=_("length"), null=True)

    host = models.ForeignKey(User, related_name='hosted_events',
                             verbose_name=_("host"))

    participants = models.ManyToManyField(User, related_name='events',
                                          verbose_name=_("participants"))

    def __str__(self):
        return "Event on {} hosted by {} with {} participants".format(
                self.date, self.host.username, self.participants.count())

    def get_absolute_url(self):
        return reverse_lazy('events:show', args=(self.id, ))

    @property
    def archived(self):
        return self.date < now()

    @property
    def ends(self):
        return self.date + self.length

    @property
    def week(self):
        return Week.withdate(self.date).week

class Game(models.Model):
    class Meta:
        verbose_name = _("game")
        verbose_name_plural = _("games")

    event = models.ForeignKey(Event, related_name='games',
                              verbose_name=_("event"))

    name = models.CharField(max_length=256, verbose_name=_("name"))

    def __str__(self):
        return self.name
