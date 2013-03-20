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

import unittest
from nose.tools import eq_

import rube
from utils import prompt_for_auth


class TestEasyFix(unittest.TestCase):
    def setUp(self):
        self.auth = prompt_for_auth("FAS")
        self.driver = rube.get_driver()

    def test_title(self):
        self.driver.get("https://stg.fedoraproject.org/easyfix/")
        eq_("Fedora Project easyfix", self.driver.title)