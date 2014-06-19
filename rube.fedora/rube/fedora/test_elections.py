# -*- coding: utf-8 -*-
# This file is part of Rube.
#
# Rube is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Rube is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Rube.  If not, see <http://www.gnu.org/licenses/>.

import rube.core
import rube.fedora

from selenium.webdriver.common.keys import Keys


class TestElections(rube.fedora.FedoraRubeTest):
    base = "https://admin.stg.fedoraproject.org/voting"
    title = "Fedora Elections"

    @rube.core.tolerant()
    def test_login(self):
        self.driver.get(self.base)
        elem = self.driver.find_element_by_css_selector("#loginInfo > a")
        elem.click()

        self.do_openid_login(last_click=False)

        self.wait_for("Elections")
