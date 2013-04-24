
import rube.core
import rube.fedora

from selenium.webdriver.common.keys import Keys


class TestElections(rube.fedora.FedoraRubeTest):
    base = "https://admin.stg.fedoraproject.org/voting"
    title = "Fedora Elections"

    @rube.core.tolerant()
    def test_login(self):
        self.driver.get(self.base)
        elem = self.driver.find_element_by_css_selector("input.button")
        elem.click()

        elem = self.driver.find_element_by_css_selector("#user_name")
        elem.send_keys(self.auth[0])
        elem = self.driver.find_element_by_css_selector("#password")
        elem.send_keys(self.auth[1])
        elem.send_keys(Keys.RETURN)

        self.wait_for("Welcome, %s" % self.auth[0])
