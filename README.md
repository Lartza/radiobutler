# radiodns
[![Build Status](https://drone.ltn.fi/api/badges/mervij/radiodns/status.svg)](https://drone.ltn.fi/mervij/radiodns)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Creating RadioDNS-application for Radio Moreeni.

Django + React powered service for providing RadioDNS services.

## Deployment
Deployment of project and Artemis is possible manually or in Docker.

Instructions are located in the [admin documentation.](https://radiodns.ltn.fi/docs/admin/index.html)
Installation instructions are currently available for CentOS 8 using the standalone-http docker-compose example.

### General deployment requirements
- 1.5GB of RAM, mostly for Apache Artemis.
- Using Docker requires around 3GB of disk space.
- Python 3.6+
- Node and NPM (frontend build, Node 16 tested)
- gettext for compiling Django translations
- Stomp server for Visual Slideshow
    - Apache ActiveMQ Artemis tested. Uses a 1GB Java heap by default.
    - RabbitMQ NOT supported
- (Optional) PostgreSQL, MariaDB etc. Edit `radiodns\settings.py`. SQLite3 is used by default and works well, example of PostgreSQL (and possibly MariaDB) deployments in the future.

## Development
### Requirements
- Python 3.6+
- Node and NPM
- (Optional) gettext, making and compiling Django translations
- (Optional) Stomp server for Visual Slideshow
    - Apache ActiveMQ Artemis tested
    - RabbitMQ NOT supported
    

### Setup
To set up a local development environment after cloning follow these instructions.

Creating a venv is highly recommended\
You can let your chosen IDE handle this or run\
`python -m venv venv`\
on some systems using `python3` instead of `python` is required.

You can read more about how to use one (activate etc.) on https://docs.python.org/3/library/venv.html

To fetch all Python requirements and development requirements run\
`pip install -r requirements-dev.txt`\
The other requirements files are included in requirements-dev.txt.

To fetch Node requirements run\
`npm install --prefix ./frontend`\
If you run into errors about missing `package.json`, especially on Windows, run just `npm install` inside the `frontend` folder instead.

To build the frontend components run\
`npm run --prefix ./frontend dev`\
Or again just `npm run dev` inside the `frontend` folder.

Configure `radiodns\settings.py` as required and run\
`python manage.py migrate`\
to process database migrations.

You can create an admin user for testing with\
`python manage.py createsuperuser`

Run the Django development server with\
`python mange.py runserver`

#### Build translations
Django translations require gettext to be installed. For Windows it can be obtained [here](https://mlocati.github.io/articles/gettext-iconv-windows.html)
After gettext is installed just run `python manage.py compilemessages`

#### Build documentation
To build the documentation, run `make html` in the `docs` folder.

#### Linting

To run linters and tests use the following\
`npx --prefix ./frontend eslint --ext .js,.jsx frontend/src`\
or `npx eslint --ext .js,.jsx src`
```
prospector
pydocstyle

python manage.py test
```
or with coverage
```
coverage run manage.py test
coverage report
```
