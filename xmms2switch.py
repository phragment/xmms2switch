#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Copyright © 2012 Thomas Krug
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from optparse import OptionParser
import xmmsclient
import os
import sys

parser = OptionParser()

parser.add_option("-n", "--next",
                  action="store_true", dest="next", default=False,
                  help="switch to next playlist")

parser.add_option("-p", "--prev",
                  action="store_true", dest="prev", default=False,
                  help="switch to previous playlist")

(options, args) = parser.parse_args()

if options.next and options.prev:
    parser.error("options -n and -p are mutually exclusive")
    sys.exit(1)


xmms = xmmsclient.XMMSSync("xmms2switch")

try:
    xmms.connect(os.getenv("XMMS_PATH"))
except IOError, detail:
    print "Error:", detail
    sys.exit(1)


playlist_cur = xmms.playlist_current_active()
position_cur = 0

position = 0
playlists = []
for playlist in xmms.playlist_list():
    if not playlist.startswith("_"):
        playlists.append(playlist)
        if playlist == playlist_cur:
            position_cur = position
        position += 1


if options.next:
    position_new = position_cur + 1
    if position_new >= position:
        position_new -= position
    xmms.playlist_load(playlists[position_new])

if options.prev:
    position_new = position_cur - 1
    if position_new < 0:
        position_new += position
    xmms.playlist_load(playlists[position_new])

xmms.disconnect()

