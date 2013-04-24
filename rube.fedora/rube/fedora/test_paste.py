
import rube.core
import rube.fedora
import uuid


class TestFPaste(rube.fedora.FedoraRubeTest):
    base = "http://paste.stg.fedoraproject.org/"
    title = u'New paste \u2022 Fedora Project Pastebin'

    @rube.core.tolerant()
    def test_paste(self):
        self.driver.get("http://paste.stg.fedoraproject.org/")

        elem = self.driver.find_element_by_css_selector("#paste_user")
        elem.send_keys(" (Rube Goldberg)")

        tag = str(uuid.uuid4())
        elem = self.driver.find_element_by_css_selector("#paste_data")
        elem.send_keys("A test message from Rube\n")
        elem.send_keys(tag)

        elem = self.driver.find_element_by_css_selector("#paste_password")
        elem.send_keys("awesome")

        elem = self.driver.find_element_by_css_selector("#paste_button")
        elem.click()
        #elem.submit()

        self.wait_for("Your paste has been saved")

        sel = "div.alert.stretch.visible.alert-green a:last-child"
        elem = self.driver.find_element_by_css_selector(sel)
        self.driver.get(elem.get_attribute("href"))

        elem = self.driver.find_element_by_css_selector("#password")
        elem.send_keys("awesome")
        elem = self.driver.find_element_by_css_selector("#pass_submit")
        elem.submit()

        self.wait_for(tag)
