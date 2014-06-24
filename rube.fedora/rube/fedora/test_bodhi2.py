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
import uuid

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import title_is


class TestBodhi2(rube.fedora.FedoraRubeTest):
    base = "http://bodhi.dev.fedoraproject.org"
    title = "Fedora Updates System"
    logout_url = base + '/logout'

    @rube.core.tolerant()
    def test_basic_functionality(self):
        self.driver.get(self.base + "/login")
        assert title_is("Login"), self.driver.title
        self.driver.get(self.base + "/login")
        self.do_openid_login(last_click=False)
        self.wait_for("Logout")

        # Ensure the datagrepper widget got injected
        assert self.driver.find_element_by_id('datagrepper-widget')
