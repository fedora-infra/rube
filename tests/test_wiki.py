from selenium import webdriver
import unittest
from nose.tools import eq_

from utils import prompt_for_auth

class TestWiki(unittest.TestCase):
    def setUp(self):
        self.auth = prompt_for_auth("FAS")
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()

    def test_title(self):
        self.driver.get("https://stg.fedoraproject.org/wiki/Fedora_Project_Wiki")
        eq_("FedoraProject", self.driver.title)

    def test_login(self):
        self.driver.get("https://stg.fedoraproject.org/wiki/Fedora_Project_Wiki")
        eq_("FedoraProject", self.driver.title)
        elem = self.driver.find_element_by_id("pt-login")
        elem.click()
        eq_("Log in - FedoraProject", self.driver.title)
