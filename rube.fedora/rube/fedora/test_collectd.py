# This file is part of Rube.
#
# Rube is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Rube is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Rube. If not, see <http://www.gnu.org/licenses/>.

import rube.core
import rube.fedora


class TestCollectd(rube.fedora.FedoraRubeTest):
    base = "https://admin.stg.fedoraproject.org/collectd/"
    title = "collection.cgi, Version 3"
    no_auth = True

    @rube.core.tolerant()
    def test_app01_page(self):
        url = self.base + "bin/index.cgi" + \
            "?hostname=app01&plugin=apache&timespan=86400" + \
            "&action=show_selection&ok_button=OK"
        self.driver.get(url)
        self.wait_for("ApacheBytes")
