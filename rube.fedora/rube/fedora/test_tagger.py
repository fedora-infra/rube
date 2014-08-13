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
from selenium.webdriver.common.keys import Keys


class TestTagger(rube.fedora.FedoraRubeTest):
    base = "https://apps.stg.fedoraproject.org/tagger"
    title = "Fedora Tagger"
    logout_url = [
        base + "/logout",
        "https://id.stg.fedoraproject.org/logout/",
    ]

    @rube.core.tolerant()
    def test_stuff(self):
        self.driver.get(self.base)
        self.wait_for('report bugs')

        selector = ".userinfo button"
        button = self.driver.find_element_by_css_selector(selector)
        button.click()

        self.do_openid_login()

        # Back to tagger
        self.wait_for("Logout")
        assert 'Score' in self.driver.page_source

        # This would be cool... but its actually broken in stg.
        ## Do a search
        #selector = ".searchbox-onpage input"
        #elem = self.driver.find_element_by_css_selector(selector)
        #elem.send_keys('nethack')
        #elem.send_keys(Keys.RETURN)

        # Instead of searching.. just do this.
        self.driver.get(self.base + "/pkgwat")

        # Ensure that we got to a page.
        self.wait_for("pkgwat")
        assert "pkgwat" in self.driver.page_source

        # Now, add a random tag and wait for the popup
        tag = str(uuid.uuid4()).split('-')[-1]
        target = 'Tag "%s" added' % tag
        elem = self.driver.find_element_by_css_selector('body')
        elem.send_keys('a')
        elem = self.driver.find_element_by_css_selector('#add_box')
        elem.send_keys(tag)
        elem.send_keys(Keys.RETURN)
        self.wait_for(target)
        #assert target in self.driver.page_source
