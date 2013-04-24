
import rube.core
import rube.fedora

from selenium.webdriver.common.keys import Keys


class TestPackages(rube.fedora.FedoraRubeTest):
    base = "https://apps.stg.fedoraproject.org/packages/"
    title = "Fedora Packages Search"
    no_auth = True

    # If memcached is down, this will fail.
    @rube.core.tolerant()
    def test_search(self):
        self.driver.get(self.base)
        elem = self.driver.find_element_by_css_selector(".grid_20 input")
        elem.send_keys("nethack")
        elem.send_keys(Keys.RETURN)

        elem = self.driver.find_element_by_css_selector(".moksha-grid-row_0 a")
        elem.click()
