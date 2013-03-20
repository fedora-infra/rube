import logging
selenium_logger = logging.getLogger("selenium.webdriver")
selenium_logger.setLevel(logging.INFO)

import nose.tools.nontrivial
import threading
import sys
import time
import zmq

from selenium import webdriver

driver = None


def get_driver():
    global driver
    if not driver:
        driver = webdriver.Firefox()
    return driver


def tearDown():
    if driver:
        driver.close()


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
