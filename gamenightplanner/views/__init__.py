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

__all__ = ['account', 'calendar', 'events', 'MainView']

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

class CreateViewWithInlines(CreateView):
    inlines = {}

    def get_context_data(self, **kwargs):
        for formset in self.inlines.keys():
            if formset not in kwargs:
                formset_kwargs = {}
                if self.request.method in ('POST', 'PUT'):
                    formset_kwargs['data'] = self.request.POST
                if self.object:
                    formset_kwargs['instance'] = self.object
                kwargs[formset] = self.inlines[formset](**formset_kwargs)
        return super().get_context_data(**kwargs)

    def all_valid(self, form, **formsets):
        self.object = form.save()
        for name, formset in formsets.items():
            formset.instance = self.object
            formset.save()
        return self.form_valid(form)

    def all_invalid(self, form, **formsets):
        return self.render_to_response(self.get_context_data(form=form,
                                                             **formsets))

    def post(self, request, *args, **kwargs):
        self.object = None
        invalid = False

        form = self.get_form()
        if not form.is_valid():
            invalid = True

        formsets = {}
        for name, formset in self.inlines.items():
            formsets[name] = formset(request.POST)
            if not formsets[name].is_valid():
                invalid = True

        if invalid:
            return self.all_invalid(form, **formsets)
        else:
            return self.all_valid(form, **formsets)

class MainView(TemplateView):
    template_name = 'gamenightplanner/main.html'
