
import rube.core
import rube.fedora
import uuid

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import title_is


class TestWiki(rube.fedora.FedoraRubeTest):
    base = "https://stg.fedoraproject.org/wiki"
    logout_url = "https://stg.fedoraproject.org/w/index.php" + \
        "?title=Special:UserLogout"
    title = "FedoraProject"

    @rube.core.tolerant()
    @rube.core.expects_zmqmsg('stg.wiki.article.edit')
    def test_login_and_edit(self):
        self.driver.get(self.base + "/Fedora_Project_Wiki")
        assert title_is(self.title), self.driver.title
        elem = self.driver.find_element_by_id("pt-login")
        elem.click()

        assert title_is("Log in - " + self.title), self.driver.title
        elem = self.driver.find_element_by_id("wpName1")
        elem.send_keys(self.auth[0])
        elem = self.driver.find_element_by_id("wpPassword1")
        elem.send_keys(self.auth[1])
        elem = self.driver.find_element_by_id("wpLoginAttempt")
        elem.submit()

        assert title_is(self.title), self.driver.title

        self.driver.get(
            "https://stg.fedoraproject.org/wiki/Rube_Test_Page")
        elem = self.driver.find_element_by_id("ca-edit")
        elem.click()

        elem = self.driver.find_element_by_id("wpTextbox1")
        elem.send_keys(Keys.PAGE_DOWN)
        tag = str(uuid.uuid4())
        s = "Test comment from Rube\n%s" % tag
        elem.send_keys(s)
        elem = self.driver.find_element_by_id("wpSave")
        elem.submit()

        self.wait_for(tag)
