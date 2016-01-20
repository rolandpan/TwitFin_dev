===========
TwitFin_dev
===========

``TwitFin_dev`` - Description of your python package


Features
--------

* Import Quandl data
* Convert to time series
* Perform Moving Average Convergence Divergence and flag runs
* ...
* Create or append data store (csv or SQL)
* ...


Getting started (development)
-----------------------------

First, `git clone` this repo and `cd` into the new directory.

Create a new virtual environment: `virtualenv -p python3 venv`

Activate the new environment: `source venv/bin/activate`

Install the required packages: `pip install -r requirements.txt`


Running notebook examples
-------------------------

Start the notebook server: `jupyter notebook`


Contributing
------------

Fork the repo, create a new feature branch, commit changes and submit a pull request.


==============  ==========================================================
Python support  Python 2.7, >= 3.5
Source          https://github.com/rolandpan/TwitFin
Docs            http://TwitFin.rtfd.org
Changelog       http://TwitFin.readthedocs.org/en/latest/history.html
API             http://TwitFin.readthedocs.org/en/latest/api.html
Issues          https://github.com/rolandpan/TwitFin/issues
Travis          http://travis-ci.org/rolandpan/TwitFin
Test coverage   https://coveralls.io/r/rolandpan/TwitFin
pypi            https://pypi.python.org/pypi/TwitFin
Ohloh           https://www.ohloh.net/p/TwitFin
License         `BSD`_.
git repo        .. code-block:: bash

                    $ git clone https://github.com/rolandpan/TwitFin.git
install dev     .. code-block:: bash

                    $ git clone https://github.com/rolandpan/TwitFin.git TwitFin
                    $ cd ./TwitFin
                    $ virtualenv .env
                    $ source .env/bin/activate
                    $ pip install -e .
tests           .. code-block:: bash

                    $ python setup.py test
==============  ==========================================================

.. _BSD: http://opensource.org/licenses/BSD-3-Clause
.. _Documentation: http://TwitFin.readthedocs.org/en/latest/
.. _API: http://TwitFin.readthedocs.org/en/latest/api.html
