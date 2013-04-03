# This file is part of Rube.
#
# Rube is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Rube is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Rube. If not, see <http://www.gnu.org/licenses/>.

import vault
import sys
import nose.tools.nontrivial
import threading
import time
import zmq

from functools import wraps
from testconfig import config

_cache = {}


def prompt_for_auth(service):
    global _cache

    if service in _cache:
        return _cache[service]

    original_stdout = sys.stdout
    sys.stdout = sys.stderr
    username = vault.get(service, "username")
    password = vault.get(service, "password")
    sys.stdout = original_stdout

    _cache[service] = (username, password)

    return username, password


class ZmqmsgListener(threading.Thread):
    """ A background thread that listens for ZeroMQ messages on a given topic.
    Sets a ``success`` flag to True if it sees such a message.
    """

    def __init__(self, topic, timeout):
        self.topic = topic
        self.timeout = timeout
        self.success = False
        self.die = False
        super(ZmqmsgListener, self).__init__()

    def run(self):
        start = time.time()
        ctx = zmq.Context()
        s = ctx.socket(zmq.SUB)
        if not config.get('zeromq', {}).get('endpoint', None):
            raise AttributeError(
                "ZeroMQ endpoint not defined, but is required for testing")
        endpoint = str(config.get('zeromq', {}).get('endpoint', ""))
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


def expects_zmqmsg(topic, timeout=20000):
    """ A decorator that will cause a test to fail if it does not
    produce a ZeroMQ message that *contains* the topic given here.
    """

    def decorate(func):
        name = func.__name__
        @wraps(func)
        def newfunc(*args, **kw):
            t = ZmqmsgListener(topic, timeout)
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


def tolerant(n=3):
    """ A decorator.  If the wrapped test fails, try again a number of
    times to see if we didn't just experience a network timeout.
    """

    def decorate(func):
        @wraps(func)
        def newfunc(*args, **kw):
            original_exception = None
            for i in range(n):
                try:
                    return func(*args, **kw)
                except Exception as e:
                    if not original_exception:
                        original_exception = e
                    if i == n - 1:
                        raise original_exception

        newfunc = nose.tools.nontrivial.make_decorator(func)(newfunc)
        return newfunc
    return decorate


def skip_logout():
    """ A decorator. If wrapped test will not attempt a logout via
    logout_url. Use this for testing negative cases such as bad credentials
    or when login/logout is not required.
    """
    def decorate(func):
        @wraps(func)
        def newfunc(*args, **kw):
            self = args[0].__class__
            self._no_teardown.append(args[0]._testMethodName)
            return func(*args, **kw)
        newfunc = nose.tools.nontrivial.make_decorator(func)(newfunc)
        return newfunc
    return decorate
