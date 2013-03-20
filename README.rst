::

                _
     _ __ _   _| |__   ___
    | '__| | | | '_ \ / _ \
    | |  | |_| | |_) |  __/
    |_|   \__,_|_.__/ \___|

Automated browser tests for `Fedora Infrastructure
<http://fedoraproject.org/wiki/Infrastructure>`_ with
`selenium <http://docs.seleniumhq.org/>`_.

It tests against the **staging** environment and attempts to cover
most of the apps listed at `apps.fp.o <https://apps.fedoraproject.org>`_.

Running
-------

::

    $ sudo yum install -y python-virtualenv
    $ git clone git://github.com/fedora-infra/rube.git
    $ cd rube
    $ virtualenv rube-env
    $ source rube-env/bin/activate
    $ pip install -r requirements.txt
    $ nosetests

Covered Services
----------------

Rube currently tests the following services in staging:

- https://admin.stg.fedoraproject.org/updates
- https://admin.stg.fedoraproject.org/collectd
- https://stg.fedoraproject.org/easyfix
- https://admin.stg.fedoraproject.org/voting
- https://admin.stg.fedoraproject.org/haproxy/proxy1
- https://koji.stg.fedoraproject.org/koji
- https://admin.stg.fedoraproject.org/nagios
- https://admin.stg.fedoraproject.org/pkgdb
- https://stg.fedoraproject.org/wiki
- https://pkgs.stg.fedoraproject.org/
- https://paste.stg.fedoraproject.org/

No Staging
----------

Here is a list of all the sites that do not have a staging equivalent from `apps.fp.o https://apps.fedoraproject.org`_.

- https://bugzilla.redhat.com/
- http://status.fedoraproject.org/
- https://fedorapeople.org
- http://planet.fedoraproject.org/
- http://lists.fedoraproject.org/
- https://retrace.fedoraproject.org/faf/summary/
- http://qa.fedoraproject.org/blockerbugs

Bad Certificates
----------------

Here is a list of the apps from `apps.fp.o <http://apps.fedoraproject.org>`_ that are not amenable to selenium tests due to expired certificates:

- https://ask.stg.fedoraproject.org/questions/
- https://docs.stg.fedoraproject.org/en-US/index.html
- https://apps.stg.fedoraproject.org/busmon/
- https://stg.fedorahosted.org/
- https://apps.stg.fedoraproject.org/packages/
- https://mirrors.stg.fedoraproject.org/publiclist/

Authors
-------

- `Ralph Bean <http://threebean.org>`_
- `Remy DeCausemaker <http://decausemaker.org>`_
- `Luke Macken <http://lewk.org>`_

License
-------
Rube is free software: you can redistribute it and/or modify it under the terms
of the GNU Affero General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

Rube is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU Affero General Public License along
with Rube. If not, see `gnu.org/licenses <http://www.gnu.org/licenses/>`_.

.. image:: https://www.gnu.org/graphics/agplv3-155x51.png
