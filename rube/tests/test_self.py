""" A self test. """

import rube
from nose.tools import raises


@raises(AssertionError)
@rube.expects_fedmsg("fake_topic", timeout=1)
def test_expects_fedmsg():
    """ Test that the decorator raises the correct error if
    no fedmsg message is found.
    """
    pass
