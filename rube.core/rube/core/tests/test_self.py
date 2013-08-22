# -*- coding: utf-8 -*-
# This file is part of Rube.
#
# Rube is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Rube is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Rube.  If not, see <http://www.gnu.org/licenses/>.
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


def fail():
    assert False


def win():
    assert True


@raises(AssertionError)
@rube.core.ensures_after(fail)
def test_after_callable_failure():
    """ Test that the after callable correctly fails. """
    pass


@rube.core.ensures_after(win)
def test_after_callable_success():
    """ Test that the after callable doesn't give false positives. """
    pass
