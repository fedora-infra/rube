import logging
selenium_logger = logging.getLogger("selenium.webdriver")
selenium_logger.setLevel(logging.INFO)

import unittest
import nose.tools.nontrivial
import threading
import time
import zmq
import selenium.webdriver.support.ui as ui

from selenium import webdriver
from utils import prompt_for_auth
from nose.tools import eq_

driver = None


def get_driver():
    global driver
    if not driver:
        driver = webdriver.Firefox()
    return driver


def tearDown():
    if driver:
        driver.close()


class RubeTest(unittest.TestCase):
    base = None
    title = None
    logout_url = None
    timeout = 20000

    def setUp(self):
        self.driver = get_driver()
        self.auth = prompt_for_auth("FAS")

    def tearDown(self):
        if self.logout_url:
            self.driver.get(self.logout_url)

    def wait_for(self, target):
        wait = ui.WebDriverWait(self.driver, self.timeout)
        wait.until(lambda d: target in d.page_source)

    def test_title(self):
        self.driver.get(self.base)
        eq_(self.title, self.driver.title)


class FedmsgListener(threading.Thread):
    """ A background thread that listens for fedmsg messages on a given topic.
    Sets a ``success`` flag to True if it sees such a message.
    """

    def __init__(self, topic, timeout):
        self.topic = topic
        self.timeout = timeout
        self.success = False
        self.die = False
        super(FedmsgListener, self).__init__()

    def run(self):
        start = time.time()
        ctx = zmq.Context()
        s = ctx.socket(zmq.SUB)
        endpoint = "tcp://stg.fedoraproject.org:9940"
        s.connect(endpoint)
        s.setsockopt(zmq.SUBSCRIBE, '')
        poller = zmq.Poller()
        poller.register(s, zmq.POLLIN)
        while not self.die:
            evts = poller.poll(100)
            if evts:
                topic, msg = s.recv_multipart()
                if self.topic in topic:
                    self.success = True
                    self.die = True
            if time.time() - start > self.timeout:
                self.die = True


def expects_fedmsg(topic, timeout=20000):
    """ A decorator that will cause a test to fail if it does not
    produce a fedmsg message that *contains* the topic given here.
    """

    def decorate(func):
        name = func.__name__

        def newfunc(*args, **kw):
            t = FedmsgListener(topic, timeout)
            t.start()

            try:
                result = func(*args, **kw)
            except:
                t.die = True
                raise
            finally:
                t.join()

            if not t.success:
                message = "%s() did not produce msg %s" % (name, topic)
                raise AssertionError(message)

            return result

        newfunc = nose.tools.nontrivial.make_decorator(func)(newfunc)
        return newfunc
    return decorate
