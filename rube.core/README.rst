rube.core
=========

.. split here

::

                _
     _ __ _   _| |__   ___
    | '__| | | | '_ \ / _ \
    | |  | |_| | |_) |  __/
    |_|   \__,_|_.__/ \___|.core


`rube.core <https://pypi.python.org/pypi/rube.core>`_ is a convenience layer
on top of selenium; the idea was to make it easier to write new integration
tests for our staging infrastructure in a way that looked like normal old
unit tests.

Rube is developed by the `Fedora Infrastructure team
<http://fedoraproject.org/wiki/Infrastructure>`_.  You can find the tests for
*our* infrastructure in the `rube.fedora
<https://pypi.python.org/pypi/rube.fedora>`_.  Please feel free to re-use
``rube.core`` as you see fit.

If you are interested in *running the Fedora Infrastructure test suite*, please
see the ``rube.fedora`` `README
<https://github.com/fedora-infra/rube/blob/develop/rube.fedora/README.rst>`_.

Features
--------

rube.core provides a number of useful decorators for your tests.

- ``@rube.core.tolerant(n=3)`` tries to run your test.  If it succeeds, it does
  nothing more.  If your test fails, it tries again and again (up to ``n``
  times, by default 3 times).  If it fails all ``n`` times, the failure is
  reported in the test.  This is useful if your connection is flaky, or you
  know that one app is sometimes on the fritz.

- ``@rube.core.skip_logout()`` perhaps somewhat obviously will add your test to
  a hidden ``_no_teardown`` list.  The ``tearDown`` method will skip it when
  the time comes.

- ``@rube.core.expects_zmqmsg(topic, timeout=20000)`` will cause rube to start
  up a background thread with a ``zmq.SUB`` socket.  It will connect to
  whatever endpoint you have listed in ``setup.cfg`` like this::

    [zeromq]
    tcp://stg.fedoraproject.org:9940

  If a message does not arrive with the specified multipart prefix before the
  timeout has elapsed, then that test will fail.  In Fedora Infrastructure, we
  use this to ensure that actions triggered on webapps by rube cause `fedmsg
  <http://fedmsg.com>`_ messages to be published on our staging gateway.

- ``@rube.core.ensures_after(callable)`` will invoke ``callable`` after your
  test has run, giving it a chance to raise an exception.

  The common use case is to define a callable that executes a shell
  command.  For instance, you could have a selenium test that goes to an
  account system and applies for a dummy user's membership in a group.  After
  that test has run, your callable could use paramiko to ssh to a machine and
  ensure that that user now has shell access (or something).

- ``@rube.core.collect_har`` will collect HAR performance data on your
  websites.  You have to do a little extra work (including setting up
  browsermob-proxy) in order to get this work.  See below.

----

Running the tests will open up Firefox in X which is a bit of a pain
sometimes.  If you want, you can run the tests in headless mode by setting
``headless=1`` in setup.cfg.  Doing so will require that you have
``xorg-x11-server-Xvfb`` installed via yum, however.

----

Collecting HAR files for performance metrics.

Rube will output harfile data into a ``harfiles/`` directory if you turn on
``collect-har`` and specify a ``path`` to `browsermob-proxy
<http://bmp.lightbody.net>`_ in the ``[browsermob]`` section of your setup.cfg
file.

You'll also need to manually ``pip install browsermob-proxy`` into your
virtualenv.  Note that `this patch
<https://github.com/AutomatedTester/browsermob-proxy-py/pull/13>`_ is required
to collect HAR files from https sites (such as our entire infrastructure).

Authors
-------

- `Ralph Bean <http://threebean.org>`_
- `Remy DeCausemaker <http://decausemaker.org>`_
- `Luke Macken <http://lewk.org>`_
- `Ricky Elrod <http://elrod.me>`_
- `Greg Jurman <https://github.com/gregjurman>`_

License
-------
Rube is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

Rube is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with Rube. If not, see `gnu.org/licenses <http://www.gnu.org/licenses/>`_.

.. image:: https://www.gnu.org/graphics/gplv3-127x51.png
   :target: https://www.gnu.org/licenses/gpl.txt
