django-zip-stream
=================

|Build Status| |codecov| |Code Health| |Codacy Badge| |license|

Django extension to assemble ZIP archives dynamically using Nginx with
`mod\_zip`_.

ZIP archive generation alternatives such as `ZipStream`_ can tie up web
server threads and make Python do the heavy lifting. To achieve higher
performance, django-zip-stream offloads ZIP archive generation to
Nginx/mod\_zip which frees up web servers to serve other clients.

To use this library, setup Nginx (with mod\_zip installed) as a reverse proxy for your Python web app.

Requirements
------------

-  Django 1.7 +
-  Python 2.7, 3.4, 3.5, or pypy
-  Nginx 0.7.25 or later compiled with `mod\_zip`_

See the Travis CI build matrix for detailed information regarding the
latest master.

Installation
------------

::

    pip install git+https://github.com/travcunn/django-zip-stream.git

Examples
--------

Django view that streams a zip with 2 files
'''''''''''''''''''''''''''''''''''''''''''

.. code:: python

    from django_zip_stream.responses import TransferZipResponse

    def download_zip(request):
        files = [
           ("/chicago.jpg", "/home/travis/chicago.jpg", 4096),
           ("/portland.jpg", "/home/travis/portland.jpg", 4096),
        ]
        return TransferZipResponse(filename='download.zip', files=files)

Resources
---------

-  Documentation: https://django-zip-stream.readthedocs.io
-  PyPI page: http://pypi.python.org/pypi/django-zip-stream
-  Code repository: https://github.com/travcunn/django-zip-stream
-  Bugtracker: https://github.com/travcunn/django-zip-stream/issues
-  Continuous integration:
   https://travis-ci.org/travcunn/django-zip-stream
-  Roadmap: https://github.com/travcunn/django-zip-stream/milestones

.. _mod\_zip: https://github.com/evanmiller/mod_zip
.. _ZipStream: https://github.com/SpiderOak/ZipStream

.. |Build Status| image:: https://travis-ci.org/travcunn/django-zip-stream.svg?branch=master
   :target: https://travis-ci.org/travcunn/django-zip-stream
.. |codecov| image:: https://codecov.io/gh/travcunn/django-zip-stream/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/travcunn/django-zip-stream
.. |Code Health| image:: https://landscape.io/github/travcunn/django-zip-stream/master/landscape.svg?style=flat
   :target: https://landscape.io/github/travcunn/django-zip-stream/master
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/be7b93a01ebb4fb39aa3cbdfdabfccd9
   :target: https://www.codacy.com/app/tcunningham/django-zip-stream
.. |license| image:: https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000
   :target: http://pypi.python.org/pypi/django-zip-stream
