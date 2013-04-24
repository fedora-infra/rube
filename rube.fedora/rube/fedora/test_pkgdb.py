
import rube.core
import rube.fedora

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import title_is


class TestPkgDb(rube.fedora.FedoraRubeTest):
    base = "https://admin.stg.fedoraproject.org/pkgdb"
    title = "Fedora Package Database"

    @rube.core.tolerant()
    def test_search_for_nethack(self):
        package_name = "nethack"
        self.driver.get(self.base)

        elem = self.driver.find_element_by_name("pattern")
        elem.send_keys(package_name)
        elem.send_keys(Keys.RETURN)

        self.wait_for(package_name)
        sel = "a.PackageName:first-child"
        elem = self.driver.find_element_by_css_selector(sel)
        self.driver.get(elem.get_attribute("href"))
        self.wait_for(package_name)

    @rube.core.tolerant()
    @rube.core.expects_zmqmsg('stg.pkgdb.acl.request.toggle')
    def test_login_request_acls(self):
        package_name = "ruby"  # lol

        self.driver.get(self.base + "/login")
        assert title_is("Login to the PackageDB"), self.driver.title
        elem = self.driver.find_element_by_name("user_name")
        elem.send_keys(self.auth[0])
        elem = self.driver.find_element_by_name("password")
        elem.send_keys(self.auth[1])
        elem.send_keys(Keys.RETURN)
        self.wait_for("The Fedora Project is maintained")

        elem = self.driver.find_element_by_name("pattern")
        elem.send_keys(package_name)
        elem.send_keys(Keys.RETURN)

        self.wait_for(package_name)
        sel = "a.PackageName:first-child"
        elem = self.driver.find_element_by_css_selector(sel)
        self.driver.get(elem.get_attribute("href"))
        self.wait_for(package_name)

        elem = self.driver.find_element_by_css_selector(".addMyselfButton")
        elem.click()

        elem = self.driver.find_element_by_css_selector(".aclPresentBox")
        elem.click()
        self.wait_for("Approved")

        elem = self.driver.find_element_by_css_selector(".aclPresentBox")
        elem.click()
        self.wait_for("Obsolete")
