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

from django.utils.timezone import now
from django.views.generic.base import TemplateResponseMixin, TemplateView
from django.views.generic.edit import CreateView

__all__ = ['calendar', 'events', 'MainView', 'LoginOptionsView']

class AjaxableViewMixin(TemplateResponseMixin):
    non_ajax_template_name = 'gamenightplanner/non-ajax.html'

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.template_name]
        else:
            return [self.non_ajax_template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ajax'] = self.request.is_ajax()
        context['template'] = self.template_name
        return context

class CreateWithAddedInfoMixin(CreateView):
    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.instance.added = now()
        return super().form_valid(form)

class MainView(TemplateView):
    template_name = 'gamenightplanner/main.html'

class LoginOptionsView(AjaxableViewMixin, TemplateView):
    template_name = 'gamenightplanner/login.html'
