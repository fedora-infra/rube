Rube
====

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
