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

import logging
import unittest
import selenium.webdriver.support.ui as ui

from selenium import webdriver
from nose.tools import eq_

from utils import prompt_for_auth, expects_fedmsg

selenium_logger = logging.getLogger("selenium.webdriver")
selenium_logger.setLevel(logging.INFO)

driver = None


def get_driver():
    global driver
    if not driver:
        driver = webdriver.Firefox()
    return driver


def tearDown():
    global driver
    if driver:
        driver.close()


class RubeTest(unittest.TestCase):
    base = None
    title = None
    logout_url = None
    timeout = 20000

    def setUp(self):
        self.driver = get_driver()
        self.auth = prompt_for_auth("FAS")

    def tearDown(self):
        if self.logout_url:
            self.driver.get(self.logout_url)

    def wait_for(self, target):
        wait = ui.WebDriverWait(self.driver, self.timeout)
        wait.until(lambda d: target in d.page_source)

    def test_title(self):
        self.driver.get(self.base)
        eq_(self.title, self.driver.title)


__all__ = ['RubeTest', 'expects_fedmsg', 'get_driver']
