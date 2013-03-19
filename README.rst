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
