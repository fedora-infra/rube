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
from selenium import webdriver
import unittest
from nose.tools import eq_

from utils import prompt_for_auth

class TestKoji(unittest.TestCase):
    def setUp(self):
        self.auth = prompt_for_auth("FAS")
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()

    def test_title(self):
        self.driver.get("http://koji.stg.fedoraproject.org/koji/")
        eq_("Build System Info | koji", self.driver.title)
