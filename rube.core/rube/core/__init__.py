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

from selenium.webdriver.support.expected_conditions import title_is

from pyvirtualdisplay import Display
from selenium import webdriver

from testconfig import config

from utils import prompt_for_auth, expects_zmqmsg, tolerant, skip_logout

selenium_logger = logging.getLogger("selenium.webdriver")
selenium_logger.setLevel(logging.INFO)

display = None
driver = None


def get_driver():
    global display
    global driver
    if not driver:
        if int(config.get('xconfig', {}).get('headless', 0)):
            display = Display(visible=0, size=(800, 600))
            display.start()
        driver = webdriver.Firefox()
        driver.implicitly_wait(60)
    return driver


def tearDown():
    global display
    global driver
    if driver:
        driver.close()
    if display:
        display.stop()


class RubeTest(unittest.TestCase):
    base = None
    title = None
    logout_url = None
    timeout = 20000

    # If you subclass and set this to True, then we won't prompt you for auth.
    no_auth = False
    # Change this in your subclass to use a different realm in the keyring.
    realm = None
    # Internally used to skip logout and whatnot during teardown
    _no_teardown = []

    def setUp(self):
        self.driver = get_driver()
        self.driver.delete_all_cookies()

        # not no_auth ~= yes auth
        if not self.no_auth and self.realm:
            self.auth = prompt_for_auth(self.realm)

    def tearDown(self):
        if self._testMethodName in self._no_teardown:
            return  # skip the teardown

        if not self.no_auth and self.logout_url:
            self.driver.get(self.logout_url)

    def wait_for(self, target):
        wait = ui.WebDriverWait(self.driver, self.timeout)
        wait.until(lambda d: target in d.page_source)

    @tolerant()
    def test_title(self):
        self.driver.get(self.base)
        assert title_is(self.title), self.driver.title


__all__ = [
    'RubeTest',
    'expects_zmqmsg',
    'tolerant',
    'get_driver',
    'skip_logout'
]
