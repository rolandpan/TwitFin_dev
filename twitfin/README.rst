===========
twitfin_dev
===========

``twitfin_dev`` - Description of your python package


Features
--------

* Import Quandl data
* Convert to time series
* Perform Moving Average Convergence Divergence and flag flips
* ...
* Create or append data store (csv or SQL)
* ...


Getting started (development)
-----------------------------

First, ``git clone`` this repo and ``cd`` into the new directory.

Create a new virtual environment: ``virtualenv venv``

Activate the new environment: ``source venv/bin/activate``

Install the required packages: ``pip install -r requirements.txt``

Set environment variables if accessing the Quandl API: ``export QUANDL_TOKEN="your-secret-key"``


Running examples.py
-----------------

Run: ``python examples.py``


Running notebooks
-----------------

Step into the notebooks directory: ``cd notebooks``

Start the notebook server with the command: ``jupyter notebook``

Interact with the notebooks in your browser at ``http://localhost:8888``


Package info
------------

==============  ==========================================================
Python support  Python 2.7, >= 3.5
Source          https://github.com/rolandpan/twitfin
Docs            http://twitfin.rtfd.org
Changelog       http://twitfin.readthedocs.org/en/latest/history.html
API             http://twitfin.readthedocs.org/en/latest/api.html
Issues          https://github.com/rolandpan/twitfin/issues
Travis          http://travis-ci.org/rolandpan/twitfin
Test coverage   https://coveralls.io/r/rolandpan/twitfin
pypi            https://pypi.python.org/pypi/twitfin
Ohloh           https://www.ohloh.net/p/twitfin
License         `BSD`_.
git repo        .. code-block:: bash

                    $ git clone https://github.com/rolandpan/twitfin.git
install dev     .. code-block:: bash

                    $ git clone https://github.com/rolandpan/twitfin.git twitfin
                    $ cd ./twitfin
                    $ virtualenv .env
                    $ source .env/bin/activate
                    $ pip install -e .
tests           .. code-block:: bash

                    $ python setup.py test
==============  ==========================================================

.. _BSD: http://opensource.org/licenses/BSD-3-Clause
.. _Documentation: http://twitfin.readthedocs.org/en/latest/
.. _API: http://twitfin.readthedocs.org/en/latest/api.html


Contributing
------------

Refer to CONTRIBUTING.rst
