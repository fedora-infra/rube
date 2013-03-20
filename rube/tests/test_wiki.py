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

import rube
import time
import uuid

from nose.tools import eq_
from selenium.webdriver.common.keys import Keys


class TestWiki(rube.RubeTest):
    base = "https://stg.fedoraproject.org/wiki"
    logout_url = "https://stg.fedoraproject.org/w/index.php" + \
        "?title=Special:UserLogout"
    title = "FedoraProject"

    @rube.expects_fedmsg('stg.wiki.article.edit')
    def test_login_and_edit(self):
        self.driver.get(self.base + "/Fedora_Project_Wiki")
        eq_("FedoraProject", self.driver.title)
        elem = self.driver.find_element_by_id("pt-login")
        elem.click()

        time.sleep(1)
        eq_("Log in - FedoraProject", self.driver.title)
        elem = self.driver.find_element_by_id("wpName1")
        elem.send_keys(self.auth[0])
        elem = self.driver.find_element_by_id("wpPassword1")
        elem.send_keys(self.auth[1])
        elem = self.driver.find_element_by_id("wpLoginAttempt")
        elem.submit()

        time.sleep(1)
        eq_("FedoraProject", self.driver.title)

        self.driver.get(
            "https://stg.fedoraproject.org/wiki/Rube_Test_Page")
        elem = self.driver.find_element_by_id("ca-edit")
        elem.click()
        time.sleep(1)

        elem = self.driver.find_element_by_id("wpTextbox1")
        elem.send_keys(Keys.PAGE_DOWN)
        tag = str(uuid.uuid4())
        s = "Test comment from Rube\n%s" % tag
        elem.send_keys(s)
        elem = self.driver.find_element_by_id("wpSave")
        elem.submit()

        time.sleep(1)
        self.wait_for(tag)
