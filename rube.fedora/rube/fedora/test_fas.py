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


class TestFas(rube.fedora.FedoraRubeTest):
    base = "https://admin.stg.fedoraproject.org/accounts"
    logout_url = "https://admin.stg.fedoraproject.org/accounts/logout"
    title = "Welcome to FAS2"

    @rube.core.tolerant()
    @rube.core.expects_zmqmsg('stg.fas.user.update')
    def test_login_and_edit_account(self):
        self.driver.get(self.base)
        assert title_is(self.title), self.driver.title
        elem = self.driver.find_element_by_link_text("Log In")
        elem.click()

        title = "Login to the Fedora Accounts System"
        assert title_is(title), self.driver.title
        elem = self.driver.find_element_by_name("user_name")
        elem.send_keys(self.auth[0])
        elem = self.driver.find_element_by_name("password")
        elem.send_keys(self.auth[1])
        elem = self.driver.find_element_by_name("login")
        elem.send_keys(Keys.ENTER)

        title = "Fedora Accounts System"
        assert title_is(title), self.driver.title

        elem = self.driver.find_element_by_link_text("My Account")
        elem.click()

        elem = self.driver.find_element_by_link_text("(edit)")
        elem.click()

        elem = self.driver.find_element_by_name("comments")
        elem.send_keys(Keys.PAGE_DOWN)
        tag = str(uuid.uuid4())
        s = "Test comment from Rube\n%s" % tag
        elem.send_keys(s)
        elem = self.driver.find_element_by_xpath(
            "/html/body/div/div[4]/div[2]/form/div[15]/input")
        elem.submit()

        self.wait_for(tag)
