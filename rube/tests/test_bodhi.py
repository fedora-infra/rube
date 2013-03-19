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
#
# Authors:
#     Ralph Bean <rbean@redhat.com>
#     Remy DeCausemaker <remyd@civx.us>

from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import unittest
import uuid
import time
from nose.tools import eq_

from utils import prompt_for_auth
import rube

class TestBodhi(unittest.TestCase):
    timeout = 10
    base = "https://admin.stg.fedoraproject.org/updates"

    def setUp(self):
        self.driver = rube.get_driver()
        self.auth = prompt_for_auth("FAS")

    def tearDown(self):
        self.driver.get(self.base + "/logout")
        self.wait_for("You have successfully logged out.")

    def wait_for(self, target):
        wait = ui.WebDriverWait(self.driver, self.timeout)
        wait.until(lambda d: target in d.page_source)

    def test_title(self):
        self.driver.get(self.base)
        eq_("Fedora Update System", self.driver.title)

    def test_login(self):
        self.driver.get(self.base + "/login")
        eq_("Login", self.driver.title)
        elem = self.driver.find_element_by_name("user_name")
        elem.send_keys(self.auth[0])
        elem = self.driver.find_element_by_name("password")
        elem.send_keys(self.auth[1])
        elem.send_keys(Keys.RETURN)
        self.wait_for("Logout")

    def test_update_view(self):
        self.driver.get(self.base + "/login")
        eq_("Login", self.driver.title)

        elem = self.driver.find_element_by_name("user_name")
        elem.send_keys(self.auth[0])
        elem = self.driver.find_element_by_name("password")
        elem.send_keys(self.auth[1])
        elem.send_keys(Keys.RETURN)
        time.sleep(2)

        sel = "#comments.grid tr:first-child td:first-child a"
        elem = self.driver.find_element_by_css_selector(sel)
        self.driver.get(elem.get_attribute("href"))
        self.wait_for("Status:")

    @rube.expects_fedmsg('stg.bodhi.update.comment')
    def test_update_comment(self):
        self.driver.get(self.base + "/login")
        eq_("Login", self.driver.title)

        elem = self.driver.find_element_by_name("user_name")
        elem.send_keys(self.auth[0])
        elem = self.driver.find_element_by_name("password")
        elem.send_keys(self.auth[1])
        elem.send_keys(Keys.RETURN)

        time.sleep(1)
        sel = "#comments.grid tr:first-child td:first-child a"
        elem = self.driver.find_element_by_css_selector(sel)
        self.driver.get(elem.get_attribute("href"))
        self.wait_for("Status:")
        sel = "#addcomment a"
        elem = self.driver.find_element_by_css_selector(sel)
        elem.click()

        time.sleep(1)
        sel = "#form_text"
        elem = self.driver.find_element_by_css_selector(sel)
        tag = str(uuid.uuid4())
        s = "Test comment from http://github.com/fedora-infra/rube\n%s" % tag
        elem.send_keys(s)
        s = "input.submitbutton"
        elem = self.driver.find_element_by_css_selector(sel)
        elem.submit()

        time.sleep(1)
        self.wait_for(tag)
