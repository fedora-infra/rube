""" A self test. """

import rube.core
from nose.tools import raises


@raises(AssertionError)
@rube.core.expects_zmqmsg("fake_topic", timeout=1)
def test_expects_fedmsg():
    """ Test that the decorator raises the correct error if
    no fedmsg message is found.
    """
    pass


@raises(AssertionError)
@rube.core.tolerant()
def test_tolerant():
    raise AssertionError("This should fail")
