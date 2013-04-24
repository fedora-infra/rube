
import rube.core
import rube.fedora

from selenium.webdriver.common.keys import Keys


class TestBlockerBugs(rube.fedora.FedoraRubeTest):
    base = "https://qa.stg.fedoraproject.org/blockerbugs"
    title = "Fedora Blocker Bugs"
    logout_url = base + '/logout'

    @rube.core.tolerant()
    def test_stuff(self):
        self.driver.get(self.base)
        elem = self.driver.find_element_by_css_selector('.login-link')
        elem.click()
        elem = self.driver.find_element_by_name('username')
        elem.send_keys(self.auth[0])
        elem = self.driver.find_element_by_name('password')
        elem.send_keys(self.auth[1])
        elem.send_keys(Keys.RETURN)
        self.wait_for("Logout")

        for i in range(5):
            selector = ".menu-bar li:nth-child(%i)" % (i + 1)
            elem = self.driver.find_element_by_css_selector(selector)
            elem.click()
