from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from nose.tools import eq_

from utils import prompt_for_auth

class TestBodhi(unittest.TestCase):
    def setUp(self):
        self.auth = prompt_for_auth("FAS")
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()

    def test_title(self):
        self.driver.get("https://admin.stg.fedoraproject.org/updates")
        eq_("Fedora Update System", self.driver.title)

    def test_login(self):
        self.driver.get("https://admin.stg.fedoraproject.org/updates/login")
        eq_("Login", self.driver.title)
        elem = self.driver.find_element_by_name("user_name")
        elem.send_keys(self.auth[0])
        elem = self.driver.find_element_by_name("password")
        elem.send_keys(self.auth[1])
        elem.send_keys(Keys.RETURN)
        #self.driver.wait_for_page_to_load(10000)
        #assert("Welcome, %s" % self.auth[0] in self.driver.page)
