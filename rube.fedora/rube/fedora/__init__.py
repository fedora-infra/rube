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

from selenium.webdriver.common.keys import Keys


class FedoraRubeTest(rube.core.RubeTest):
    realm = "FAS"

    def do_openid_login(self, last_click=True):
        # Openid page
        self.wait_for("authenticate")
        elem = self.driver.find_element_by_name('username')
        elem.send_keys(self.auth[0])
        elem = self.driver.find_element_by_name('password')
        elem.send_keys(self.auth[1])
        elem.send_keys(Keys.RETURN)

        import time
        time.sleep(5)

        if 'decided_allow' in self.driver.page_source:
            # Redirect to confirm page
            elem = self.driver.find_element_by_name('decided_allow')
            elem.click()

            # And again..
            if last_click:
                sel = "input:last-child"
                elem = self.driver.find_element_by_css_selector(sel)
                elem.click()
