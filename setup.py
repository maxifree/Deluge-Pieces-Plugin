#
# setup.py
#
# Copyright (C) 2009 Nick Lanham <nick@afternight.org>
# Copyright (C) 2010 Jens Timmerman <jens.timmerman@gmail.com>
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.
#

from setuptools import setup

__plugin_name__ = "Pieces"
__author__ = "Nick Lanham"
__author_email__ = "nick@afternight.org"
__version__ = "0.6"
__url__ = "https://github.com/nicklan/Deluge-Pieces-Plugin"
__license__ = "GPLv3"
__description__ = "Add a tab showing the status of each piece of the selected torrent"
__long_description__ = """
Pieces Plugin

(c)2010 by Nick Lanham <nick@afternight.org>

This plugin adds a tab that will show the status of each piece of the
torrent.

There are three states for each piece: 
not downloaded, downloaded, or currently downloading.  
These are indicated by color.

You can easily set the priority of a piece or a set of pieces by selecting them,
right-click and set the priority.

You can select multiple pieces in a few ways.
 - Click the first piece you want to select.  Hold Shift and click the
   last piece you want to select.  All pieces in between will be
	 selected.
 - Clicking and dragging over the pieces you want to select
 - Holding Ctrl will start selecting pieces without unselecting the
   ones you have already selected


Underneath all the pieces is a checkbox that will allow you to always
prioritize the first un-downloaded piece of the torrent. This lets you
start watching a movie while it is still downloading. After completing
the torrent you should continue to seed for a while, because this
behaviour is actually not sociable and bad for the torrent
protocol. Please use with care. 
"""
__pkg_data__ = {__plugin_name__.lower(): ["template/*", "data/*"]}

setup(
    name=__plugin_name__,
    version=__version__,
    description=__description__,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license=__license__,
    long_description=__long_description__ if __long_description__ else __description__,

    packages=[__plugin_name__.lower()],
    package_data = __pkg_data__,

    entry_points="""\
[deluge.plugin.core]
%s = %s:CorePlugin
[deluge.plugin.gtkui]
%s = %s:GtkUIPlugin
[deluge.plugin.web]
%s = %s:WebUIPlugin\
""" % ((__plugin_name__, __plugin_name__.lower())*3)
)
