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


class TestPkgDb(rube.fedora.FedoraRubeTest):
    base = "https://admin.stg.fedoraproject.org/pkgdb"
    title = "Fedora Package Database"

    @rube.core.tolerant()
    def test_search_for_nethack(self):
        package_name = "nethack"
        self.driver.get(self.base)

        elem = self.driver.find_element_by_name("term")
        elem.send_keys(package_name)
        elem.send_keys(Keys.RETURN)

        self.wait_for(package_name)
        sel = "#content li a:first-child"
        elem = self.driver.find_element_by_css_selector(sel)
        self.driver.get(elem.get_attribute("href"))
        self.wait_for(package_name)

    @rube.core.tolerant()
    @rube.core.expects_zmqmsg('stg.pkgdb.acl.update')
    def test_login_request_acls(self):
        package_name = "ruby"  # lol

        self.driver.get(self.base + "/login")
        self.do_openid_login(last_click=False)

        # Back to pkgdb
        self.wait_for("log out")

        elem = self.driver.find_element_by_name("term")
        elem.send_keys(package_name)
        elem.send_keys(Keys.RETURN)

        self.wait_for(package_name)

        sel = "#content li a:first-child"
        elem = self.driver.find_element_by_css_selector(sel)
        self.driver.get(elem.get_attribute("href"))
        self.wait_for(package_name)

        # Watch the package
        sel = '[title="Request watch* ACL on all branches"]'
        elem = self.driver.find_element_by_css_selector(sel)
        elem.click()
        self.wait_for('Unwatch this package')

        # Unwatch the package
        sel = '[title="Drop your watch* ACL on all branches"]'
        elem = self.driver.find_element_by_css_selector(sel)
        elem.click()
        self.wait_for('Watch this package')

        # Request commit access
        sel = '[title="Request commit ACL on all branches"]'
        elem = self.driver.find_element_by_css_selector(sel)
        elem.click()
        self.wait_for(self.auth[0])
