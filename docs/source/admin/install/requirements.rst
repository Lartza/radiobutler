###################
System requirements
###################

******
Server
******

The following is recommended for Docker deployment.

- Linux distro with Docker support
- 2GB+ RAM when using Artemis, 4GB+ disk space
- Apache ActiveMQ Artemis 2.16+
- nginx for reverse proxying

The following is recommended for manual deployment.

- Linux
- 2GB+ RAM when using Artemis, 1.5GB+ disk space when deploying Artemis through Docker.
- Python 3.6+
- Node 15+ (older versions not tested but can be compatible)
- Apache ActiveMQ Artemis 2.16+
- nginx
- gunicorn
- (Optional) An SQL server can be used instead of SQLite

For STOMP, **RabbitMQ** is **NOT SUPPORTED**.

***********
Web browser
***********

The latest versions of the following **desktop** web browsers are supported.

- Google Chrome
- Mozilla Firefox
- Microsoft Edge
- Apple Safari