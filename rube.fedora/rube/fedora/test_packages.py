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

from selenium.webdriver.common.keys import Keys


class TestPackages(rube.fedora.FedoraRubeTest):
    base = "https://apps.stg.fedoraproject.org/packages/"
    title = "Fedora Packages Search"
    no_auth = True

    # If memcached is down, this will fail.
    @rube.core.tolerant()
    def test_search(self):
        self.driver.get(self.base)
        elem = self.driver.find_element_by_css_selector(".grid_20 input")
        elem.send_keys("nethack")
        elem.send_keys(Keys.RETURN)

        elem = self.driver.find_element_by_css_selector(".moksha-grid-row_0 a")
        elem.click()
