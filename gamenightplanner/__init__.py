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

"""Requires: Django >= 1.10, pytz, isoweek, social-auth-app-django,
django-invitations"""

default_app_config = 'gamenightplanner.apps.GameNightPlannerConfig'

VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_PATCH = ''


def get_version(numeric=False):
    if numeric:
        return (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)
    if isinstance(VERSION_PATCH, str) and VERSION_PATCH != '':
        return "{}.{}-{}".format(VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)
    elif isinstance(VERSION_PATCH, int):
        return "{}.{}.{}".format(VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)
    return "{}.{}".format(VERSION_MAJOR, VERSION_MINOR)

__VERSION__ = get_version()
