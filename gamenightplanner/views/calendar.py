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
from calendar import Calendar
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from isoweek import Week
from ..models import events


class CalendarMixin(LoginRequiredMixin):
    DAYSOFWEEK = (_('Monday'), _('Tuesday'), _('Wednesday'),
                  _('Thursday'), _('Friday'), _('Saturday'),
                  _('Sunday'))
    DAYSOFWEEK_SHORT = (_('Mon'), _('Tue'), _('Wed'), _('Thu'),
                        _('Fri'), _('Sat'), _('Sun'))
    MONTHS = (_('January'), _('February'), _('March'), _('April'),
              _('May'), _('June'), _('July'), _('August'),
              _('September'), _('October'), _('November'),
              _('December'))

    def month_link(self, year, month):
        if month <= 0:
            month = 12 - month
            year -= 1
        elif month >= 13:
            month = month - 12
            year += 1
        return reverse('calendar:month', args=(year, month))

    def week_link(self, week):
        return reverse('calendar:week', args=(week.year, week.week))

    def day_link(self, *args):
        if len(args) == 1:
            date = args[0]
            return reverse('calendar:day', args=(date.year, date.month,
                                                 date.day))
        if len(args) == 3:
            year, month, day = args
            return reverse('calendar:day', args=(year, month, day))
        raise TypeError("Expected 1 or 3 arguments")


class CalendarView(AjaxableViewMixin, CalendarMixin, ListView):
    model = events.Event

    template_name = 'gamenightplanner/calendar/month.html'

    def dispatch(self, request, year=None, month=None, *args, **kwargs):
        if year is not None and month is not None:
            self.year = int(year)
            self.month = int(month)
        else:
            today = now()
            self.year = today.year
            self.month = today.month
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(date__year=self.year,
                                         date__month=self.month)

    def calendar_iter(self):
        calendar = Calendar()
        events = self.get_queryset()
        today = date.today()
        for i, d in enumerate(calendar.itermonthdates(self.year, self.month)):
            classes = []
            if i % 7 == 0:
                week_n = d.isocalendar()[1]
                week = []
            if d == today:
                classes.append('today')
            week.append((d, events.filter(date__day=d.day), classes))
            if i % 7 == 6:
                yield week_n, week

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.year
        context['month'] = self.month
        context['monthname'] = self.MONTHS[self.month-1]
        context['monthnames'] = self.MONTHS
        context['daysofweeknames'] = self.DAYSOFWEEK
        context['daysofweekshort'] = self.DAYSOFWEEK_SHORT
        context['current_url'] = self.month_link(self.year, self.month)
        context['next_url'] = self.month_link(self.year, self.month+1)
        context['prev_url'] = self.month_link(self.year, self.month-1)
        context['calendar'] = self.calendar_iter()
        return context


class WeekView(AjaxableViewMixin, CalendarMixin, ListView):
    model = events.Event
    context_object_name = 'events'

    template_name = 'gamenightplanner/calendar/week.html'

    def dispatch(self, request, year, week, *args, **kwargs):
        self.week = Week(int(year), int(week))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(date__date__gte=self.week.monday(),
                                         date__date__lte=self.week.sunday())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.week.year
        context['month'] = self.week.monday().month
        context['week'] = self.week
        context['daysofweeknames'] = self.DAYSOFWEEK
        context['daysofweekshort'] = self.DAYSOFWEEK_SHORT
        context['current_url'] = self.week_link(self.week)
        context['next_url'] = self.week_link(self.week+1)
        context['prev_url'] = self.week_link(self.week-1)
        return context


class DayView(AjaxableViewMixin, CalendarMixin, ListView):
    model = events.Event
    context_object_name = 'events'

    template_name = 'gamenightplanner/calendar/day.html'

    def dispatch(self, request, year, month, day, *args, **kwargs):
        self.date = date(int(year), int(month), int(day))
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(date__date=self.date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = self.date
        context['year'] = self.date.year
        context['month'] = self.date.month
        context['day'] = self.date.day
        context['monthname'] = self.MONTHS[self.date.month-1]
        context['dayofweekname'] = self.DAYSOFWEEK[self.date.weekday()]
        context['dayofweekshort'] = self.DAYSOFWEEK_SHORT[self.date.weekday()]
        context['current_url'] = self.day_link(self.date)
        context['next_url'] = self.day_link(self.date.year, self.date.month,
                                            self.date.day+1)
        context['prev_url'] = self.day_link(self.date.year, self.date.month,
                                            self.date.day-1)
        return context
