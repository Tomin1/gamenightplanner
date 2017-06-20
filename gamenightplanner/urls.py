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

from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout
from .views import *


urlpatterns = [
    url(r'^$', MainView.as_view(), name='main'),
    url(r'^calendar/', include([
        url(r'^$', calendar.CalendarView.as_view(), name='index'),
        url(r'^(?P<year>\d+)/(?P<month>\d+)/$',
            calendar.CalendarView.as_view(), name='month'),
        url(r'^(?P<year>\d+)/week/(?P<week>\d+)/$',
            calendar.WeekView.as_view(), name='week'),
        url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
            calendar.DayView.as_view(), name='day'),
    ], namespace='calendar')),
    url(r'^event/', include([
        url(r'^(?P<pk>\d+)/$', events.EventDetailView.as_view(), name='show'),
        url(r'^add/$', events.CreateEventView.as_view(), name='add'),
        url(r'^add/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/' +
            r'(?P<minute>\d+)/$', events.CreateEventView.as_view(),
            name='add'),
        url(r'^add/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
            events.CreateEventView.as_view(), name='add'),
        url(r'^add/(?P<year>\d+)/(?P<month>\d+)/$',
            events.CreateEventView.as_view(), name='add'),
        url(r'^add/(?P<year>\d+)/week/(?P<week>\d+)/$',
            events.CreateEventView.as_view(), name='add-on-week'),
        url(r'^participate/(?P<pk>\d+)/$',
            events.EventDetailView.add_participation_view, name='participate'),
        url(r'^leave/(?P<pk>\d+)/$',
            events.EventDetailView.remove_participation_view, name='leave'),
    ], namespace='events')),
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include([
        url(r'^login/$', account.LoginOptionsView.as_view(), name='login'),
        url(r'^logout/$', logout, name='logout'),
        url(r'^signup/$', account.SignupView.as_view(), name='signup'),
        url(r'^signup/(?P<token>\w+)/$', account.SignupFormView.as_view(),
            name='signup-form'),
    ], namespace='account')),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^invitations/', include('invitations.urls',
        namespace='invitations')),
]
