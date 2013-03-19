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

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from nose.tools import eq_, assert_in

from utils import prompt_for_auth


class TestBodhi(unittest.TestCase):
    def setUp(self):
        self.auth = prompt_for_auth("FAS")
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()

    def test_title(self):
        self.driver.get("https://admin.stg.fedoraproject.org/updates")
        eq_("Fedora Update System", self.driver.title)

    def test_login(self):
        self.driver.get("https://admin.stg.fedoraproject.org/updates/login")
        eq_("Login", self.driver.title)
        elem = self.driver.find_element_by_name("user_name")
        elem.send_keys(self.auth[0])
        elem = self.driver.find_element_by_name("password")
        elem.send_keys(self.auth[1])
        elem.send_keys(Keys.RETURN)
        assert_in("Welcome, %s" % self.auth[0], self.driver.page_source)
