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

from . import (AjaxableViewMixin, CreateWithAddedInfoMixin,
               CreateViewWithInlines)
from datetime import datetime, time
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import ModelForm, ValidationError, inlineformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from isoweek import Week
from ..models import events


class CreateEventForm(ModelForm):
    class Meta:
        model = events.Event
        fields = ['date', 'length', 'host']

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < now():
            raise ValidationError(_("date can not be in the past"))
        return date

GameInlineFormSet = inlineformset_factory(events.Event, events.Game, extra=1,
                                          fields=('name',))


class CreateEventView(LoginRequiredMixin, AjaxableViewMixin,
                      CreateWithAddedInfoMixin, CreateViewWithInlines):
    form_class = CreateEventForm
    inlines = {'game_formset': GameInlineFormSet}
    template_name = 'gamenightplanner/event/add.html'

    def dispatch(self, request, year=None, month=None, day=None,
                 week=None, hour=None, minute=None, *args, **kwargs):
        self.date = None
        self.previous = None
        if year is not None:
            year = int(year)
            if month is not None:
                month = int(month)
                if day is not None:
                    day = int(day)
                    if hour is not None:
                        hour, minute = int(hour), int(minute)
                        self.date = datetime(year, month, day, hour, minute)
                    else:
                        self.date = datetime(year, month, day, 18, 0)
                    self.previous = ('calendar:day', {'year': year,
                                                      'month': month,
                                                      'day': day})
                else:
                    self.date = datetime(year, month, 1, 18, 0)
                    self.previous = ('calendar:month', {'year': year,
                                                        'month': month})
            elif week is not None:
                self.date = datetime.combine(Week(year, int(week)).monday(),
                                             time(18, 0))
                self.previous = ('calendar:week', {'year': year,
                                                   'week': week})
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        if self.date is not None:
            initial['date'] = self.date
        initial['host'] = self.request.user
        return initial

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel') is not None:
            if self.previous:
                return redirect(self.previous[0], **self.previous[1])
            else:
                return redirect('calendar:index')
        return super().post(request, *args, **kwargs)

    def all_valid(self, form, **kwargs):
        form.instance.added_by = self.request.user
        form.instance.added = now()
        return super().all_valid(form, **kwargs)


class EventDetailView(LoginRequiredMixin, AjaxableViewMixin, DetailView):
    model = events.Event
    template_name = 'gamenightplanner/event/event.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['can_edit'] = obj.has_change_permission(self.request, obj)
        context['can_delete'] = obj.has_delete_permission(self.request, obj)
        context['participating'] = self.get_object().participants.filter(
                pk=self.request.user.pk).exists()
        return context

    @staticmethod
    @login_required
    def add_participation_view(request, pk):
        event = get_object_or_404(events.Event, pk=pk)
        if event.archived:
            raise PermissionDenied
        event.participants.add(request.user)
        return redirect('events:show', pk=pk)

    @staticmethod
    @login_required
    def remove_participation_view(request, pk):
        event = get_object_or_404(events.Event, pk=pk)
        if event.archived:
            raise PermissionDenied
        event.participants.remove(request.user)
        return redirect('events:show', pk=pk)


class EventUpdateView(LoginRequiredMixin, AjaxableViewMixin, UpdateView):
    model = events.Event
    template_name = 'gamenightplanner/event/edit.html'
    fields = ('date', 'length', 'host')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel') is not None:
            return redirect('events:show', kwargs.pop('pk'))
        return super().post(request, *args, **kwargs)


class EventDeleteView(LoginRequiredMixin, AjaxableViewMixin, DeleteView):
    model = events.Event
    template_name = 'gamenightplanner/event/delete.html'

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel') is not None:
            return redirect('events:show', kwargs.pop('pk'))
        self.date = self.get_object().date
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('calendar:day', kwargs={'year': self.date.year,
                                               'month': self.date.month,
                                               'day': self.date.day})
