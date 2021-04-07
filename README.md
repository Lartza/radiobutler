# radiodns
[![Build Status](https://drone.ltn.fi/api/badges/mervij/radiodns/status.svg)](https://drone.ltn.fi/mervij/radiodns)

Creating RadioDNS-application for Radio Moreeni

## Development
### Requirements
- Python 3.6+
- Node and NPM
- _Stomp server (Apache ActiveMQ Artemis tested, required for Visual Slideshow)_

### Setup
To set up a local development environment after cloning follow these instructions.

Creating a venv is highly recommended\
You can let your chosen IDE handle this or run\
`python -m venv venv`\
on some systems using `python3` instead of `python` is required.

You can read more about how to use one (activate etc.) on https://docs.python.org/3/library/venv.html

To fetch all Python requirements and development requirements run\
`pip install -r requirements-dev.txt`\
Runtime requirements are installed by the -dev file too.

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

To run linters and tests use the following\
`npx --prefix ./frontend eslint --ext .js,.jsx frontend/src`\
or `npx --ext .js,.jsx src`
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