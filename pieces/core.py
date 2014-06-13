#
# core.py
#
# Copyright (C) 2009 Nick Lanham <nick@afternight.org>
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

from deluge.log import LOG as log
from deluge.plugins.pluginbase import CorePluginBase
import deluge.component as component
import deluge.configmanager
from deluge.core.rpcserver import export

from twisted.internet.task import LoopingCall, deferLater
from twisted.internet import reactor

DEFAULT_PREFS = {
    "not_dled_color":"#ffffff",
    "dled_color":"#5599ff",
    "dling_color":"#8dd35f"
}

class Core(CorePluginBase):
    def enable(self):
        self.config = deluge.configmanager.ConfigManager("pieces.conf", DEFAULT_PREFS)
        self.not_dled_color = self.config['not_dled_color']
        self.dled_color = self.config['dled_color']
        self.dling_color = self.config['dling_color']
        self.priority_loop = None

    def disable(self):
        pass

    def update(self):
        pass

    @export 
    def get_torrent_info(self, tid):
        tor = component.get("TorrentManager").torrents[tid]
        self.__handle_cache = tor.handle
        stat = tor.status

        plen = len(stat.pieces)
        if (plen <= 0):
            if (stat.num_pieces == 0):
                return (True, 0, None, None)
            if (stat.state == stat.seeding or stat.state == stat.finished):
                return (True, stat.num_pieces, None, None)

        peers = tor.handle.get_peer_info()
        curdl = []
        for peer in peers:
            if peer.downloading_piece_index != -1:
                curdl.append(peer.downloading_piece_index)

        curdl = dict.fromkeys(curdl).keys() 
        curdl.sort()

        return (False, plen, stat.pieces, curdl)

    @export
    def get_piece_priority(self, pid):
        return pid,self.__handle_cache.piece_priority(pid)

    @export
    def piece_priorities(self, selected, priority):
        for i in selected:
            if selected[i]: 
                self.__handle_cache.piece_priority(i,priority)

    @export
    def set_sequential_torrent(self, torr, sd):
        tm = component.get("TorrentManager").torrents[torr]
        tm.handle.set_sequential_download(sd)

    @export
    def is_sequential_torrent(self, torr):
        tm = component.get("TorrentManager").torrents[torr]
        return tm.status.sequential_download

    @export
    def set_config(self, config):
        "sets the config dictionary"
        for key in config.keys():
            self.config[key] = config[key]
        self.config.save()

    @export
    def get_config(self):
        "returns the config dictionary"
        return self.config.config
