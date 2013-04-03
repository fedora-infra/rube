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
import uuid

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import title_is


class TestBodhi(rube.fedora.FedoraRubeTest):
    base = "https://admin.stg.fedoraproject.org/updates"
    title = "Fedora Update System"
    logout_url = base + '/logout'

    @rube.core.tolerant()
    def test_login(self):
        self.driver.get(self.base + "/login")
        assert title_is("Login"), self.driver.title
        elem = self.driver.find_element_by_name("user_name")
        elem.send_keys(self.auth[0])
        elem = self.driver.find_element_by_name("password")
        elem.send_keys(self.auth[1])
        elem.send_keys(Keys.RETURN)
        self.wait_for("Logout")

    @rube.core.tolerant()
    @rube.core.skip_logout()
    def test_login_bad(self):
        self.driver.get(self.base + "/login")
        assert title_is("Login"), self.driver.title
        elem = self.driver.find_element_by_name("user_name")
        elem.send_keys(str(uuid.uuid4()))
        elem = self.driver.find_element_by_name("password")
        elem.send_keys(str(uuid.uuid4()))
        elem.send_keys(Keys.RETURN)
        self.wait_for("not correct or did not grant access to this resource")

    @rube.core.tolerant()
    def test_update_view(self):
        self.driver.get(self.base + "/login")
        assert title_is("Login"), self.driver.title

        elem = self.driver.find_element_by_name("user_name")
        elem.send_keys(self.auth[0])
        elem = self.driver.find_element_by_name("password")
        elem.send_keys(self.auth[1])
        elem.send_keys(Keys.RETURN)

        sel = "#comments.grid tr:first-child td:first-child a"
        elem = self.driver.find_element_by_css_selector(sel)
        self.driver.get(elem.get_attribute("href"))
        self.wait_for("Status:")

    @rube.core.tolerant()
    @rube.core.expects_zmqmsg('stg.bodhi.update.comment')
    def test_update_comment(self):
        self.driver.get(self.base + "/login")
        assert title_is("Login"), self.driver.title

        elem = self.driver.find_element_by_name("user_name")
        elem.send_keys(self.auth[0])
        elem = self.driver.find_element_by_name("password")
        elem.send_keys(self.auth[1])
        elem.send_keys(Keys.RETURN)

        sel = "#comments.grid tr:first-child td:first-child a"
        elem = self.driver.find_element_by_css_selector(sel)
        self.driver.get(elem.get_attribute("href"))
        self.wait_for("Status:")
        sel = "#addcomment a"
        elem = self.driver.find_element_by_css_selector(sel)
        elem.click()

        sel = "#form_text"
        elem = self.driver.find_element_by_css_selector(sel)
        tag = str(uuid.uuid4())
        s = "Test comment from http://github.com/fedora-infra/rube\n%s" % tag
        elem.send_keys(s)
        s = "input.submitbutton"
        elem = self.driver.find_element_by_css_selector(sel)
        elem.submit()

        self.wait_for(tag)
