# TwitFin_dev

### Contents
* [Dependencies](#dependencies)
* [Getting started](#quick-start)
* [Exiting & Shut down](#tear-down)
* [Development](#development)

<a name="dependencies"></a>
## Dependencies

We'll use vagrant to create a virtualbox with a linux environment, with a shared folder looking at TwitFin_dev.

Install [Vagrant](https://www.vagrantup.com/downloads.html) 1.8+

<a name="quick-start"></a>
## Getting started

After installing Vagrant, to run TwitFin_dev:

`git clone git@github.com:brennv/TwitFin_dev.git`

Step into the directory:

`cd TwitFin_dev`

Run vagrant (it will be slow the first time, but faster later):

`vagrant up`

Step into vagrant:

`vagrant ssh`

Step into the shared folder:

`cd /vagrant`

Run TwitFin:

`python run.py`


<a name="tear-down"></a>
## Exiting & Shut down

To exit vagrant, run:

`exit`

To shut down vagrant, run:

`vagrant suspend`


<a name="development"></a>
## Development

See TwitFin_dev/twitfin/README.rst

To load environment changes in vagrant, run:

`vagrant reload --provision`
