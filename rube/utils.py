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


def tolerant(n=3):
    """ A decorator.  If the wrapped test fails, try again a number of
    times to see if we didn't just experience a network timeout.
    """

    def decorate(func):
        name = func.__name__

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
