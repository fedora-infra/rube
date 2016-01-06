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

import uuid

import rube.core
import rube.fedora

from selenium.webdriver.support.expected_conditions import title_is


class TestBodhi2(rube.fedora.FedoraRubeTest):
    base = "http://bodhi.stg.fedoraproject.org"
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

        # Go to the list of updates
        self.driver.get(self.base + "/updates")

        # Get a specific update
        sel = "td > a"
        link = self.driver.find_element_by_css_selector(sel)
        link.click()
        self.wait_for("Notes about this update")

        # Comment on it
        field = self.driver.find_element_by_id('text')
        gif = "http://i.imgur.com/rhyuVf2.gif"
        idx = str(uuid.uuid4())
        s = "Test comment from [Rube](%s):\n\n* `%s`" % (gif, idx)
        field.send_keys(s)

        form = self.driver.find_element_by_css_selector("#new_comment")
        form.submit()

        self.wait_for(idx)
