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
from selenium.webdriver.support.expected_conditions import title_is


class TestBlockerBugs(rube.fedora.FedoraRubeTest):
    base = "https://qa.stg.fedoraproject.org/blockerbugs"
    title = "Fedora Blocker Bugs"
    logout_url = base + '/logout'

    @rube.core.tolerant()
    def test_login_dance(self):
        self.driver.get(self.base)
        assert title_is(self.title), self.driver.title
        self.wait_for('open source')

        elem = self.driver.find_element_by_css_selector(".login-link > a")
        elem.click()

        self.do_openid_login()

        # Back to blockerbugs
        self.wait_for("Logout")

        for i in range(5):
            selector = ".menu-bar li:nth-child(%i)" % (i + 1)
            elem = self.driver.find_element_by_css_selector(selector)
            elem.click()

    def do_openid_login(self):
        # Openid page
        self.wait_for("Create a new account")
        elem = self.driver.find_element_by_name('username')
        elem.send_keys(self.auth[0])
        elem = self.driver.find_element_by_name('password')
        elem.send_keys(self.auth[1])
        elem.send_keys(Keys.RETURN)

        # Redirect to confirm page
        elem = self.driver.find_element_by_name('decided_allow')
        elem.click()

        ## And again..
        elem = self.driver.find_element_by_css_selector("input:last-child")
        elem.click()
