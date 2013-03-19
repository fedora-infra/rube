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
#
import unittest
import uuid
import time
from nose.tools import assert_in
import selenium.webdriver.support.ui as ui

import rube
from utils import prompt_for_auth


class TestFPaste(unittest.TestCase):
    timeout = 10000

    def setUp(self):
        self.auth = prompt_for_auth("FAS")
        self.driver = rube.get_driver()

    def wait_for(self, target):
        wait = ui.WebDriverWait(self.driver, self.timeout)
        wait.until(lambda d: target in d.page_source)

    def test_title(self):
        self.driver.get("http://paste.stg.fedoraproject.org/")
        assert_in("New paste", self.driver.title)

    def test_title(self):
        self.driver.get("http://paste.stg.fedoraproject.org/")
        assert_in("New paste", self.driver.title)

        elem = self.driver.find_element_by_css_selector("#paste_user")
        elem.send_keys(" (Rube Goldberg)")

        tag = str(uuid.uuid4())
        elem = self.driver.find_element_by_css_selector("#paste_data")
        elem.send_keys("A test message from Rube\n")
        elem.send_keys(tag)

        elem = self.driver.find_element_by_css_selector("#paste_password")
        elem.send_keys("awesome")

        elem = self.driver.find_element_by_css_selector("#paste_button")
        elem.click()
        #elem.submit()

        time.sleep(1)
        self.wait_for("Your paste has been saved")

        sel = "div.alert.stretch.visible.alert-green a:last-child"
        elem = self.driver.find_element_by_css_selector(sel)
        self.driver.get(elem.get_attribute("href"))

        elem = self.driver.find_element_by_css_selector("#password")
        elem.send_keys("awesome")
        elem = self.driver.find_element_by_css_selector("#pass_submit")
        elem.submit()

        self.wait_for(tag)
