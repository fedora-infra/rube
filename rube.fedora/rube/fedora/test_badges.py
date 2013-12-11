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

from selenium.webdriver.support.expected_conditions import title_is


class TestBadges(rube.fedora.FedoraRubeTest):
    base = "https://badges.stg.fedoraproject.org"
    title = "Fedora Badges (staging!)"
    logout_url = [
        base + "/logout",
        "https://id.stg.fedoraproject.org/logout/",
    ]

    @rube.core.tolerant()
    def test_login_dance(self):
        self.driver.get(self.base)
        assert title_is(self.title), self.driver.title
        self.wait_for('free software')

        self.driver.get(self.base + "/login")

        alert = self.driver.switch_to_alert()
        alert.accept()
        self.do_openid_login(last_click=False)

        # Back to badges
        self.wait_for("Logout")

        # Go to profile
        selector = ".navbar li:nth-child(4) > a"
        elem = self.driver.find_element_by_css_selector(selector)
        elem.click()

        # Ensure that we got to the profile.
        self.wait_for("User Info")
        assert "User Info" in self.driver.page_source

        # Go to leaderboard
        selector = ".navbar li:nth-child(3) > a"
        elem = self.driver.find_element_by_css_selector(selector)
        elem.click()

        # Ensure that we got to the profile.
        self.wait_for("Leaderboard")
        assert "Leaderboard" in self.driver.page_source
