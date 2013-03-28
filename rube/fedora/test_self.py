""" A self test. """

import rube
import rube.fedora
from nose.tools import raises


@raises(AssertionError)
@rube.expects_zmqmsg("fake_topic", timeout=1)
def test_expects_fedmsg():
    """ Test that the decorator raises the correct error if
    no fedmsg message is found.
    """
    pass


@raises(AssertionError)
@rube.tolerant()
def test_tolerant():
    raise AssertionError("This should fail")
