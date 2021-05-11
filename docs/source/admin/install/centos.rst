#####################
CentOS 8 installation
#####################
The simplest way to deploy the project is using the provided standalone http docker-compose example.

Instructions assume you are on a fresh CentOS installation using an administrator user uid 1000 due to sudo and Artemis instance folder permission requirements.
The uid Artemis uses can be changed manually inside *./docker/Dockerfile-adoptopenjdk-11* after prepare but before Aremis docker build.

Install Docker

.. code-block:: console

    sudo yum install -y yum-utils
    sudo yum-config-manager --add-repo \
        https://download.docker.com/linux/centos/docker-ce.repo
    sudo yum install git patch docker-ce docker-ce-cli containerd.io
    sudo systemctl enable --now docker
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.1/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

Prepare and build Artemis Docker image

.. code-block:: console

    git clone https://github.com/apache/activemq-artemis.git
    cd activemq-artemis/artemis-docker
    ./prepare-docker.sh --from-release --artemis-version 2.17.0
    cd _TMP_/artemis/2.17.0
    sudo docker build -f ./docker/Dockerfile-adoptopenjdk-11 \
        -t artemis-adoptopenjdk-11 .

Build, configure and deploy the project

.. code-block:: console

    cd ~
    git clone https://github.com/Lartza/radiobutler
    cd radiodns
    cp docs/examples/docker-compose/standalone-http/* .
    mv radiodns.env .env
    nano .env
    mkdir artemis-instance
    sudo docker-compose up -d artemis
    sudo docker-compose stop artemis
    patch artemis-instance/etc/broker.xml < docs/artemis_broker.patch

The file artemis-instance/etc/login.config should be edited to change the default user (set in .env) and group (amq) to "guest" and "guests" respectively.
This is the user radio receivers will use to receive the slideshow.

Finally everything can be brought up.

.. code-block:: console

    sudo docker-compose up -d

The service is now available locally from http://127.0.0.1:8080 and should be reverse proxied to serve to the internet through https.
An example nginx configuration for this is available here_.

.. _here: https://github.com/Lartza/radiobutler/docs/examples/docker-compose/standalone-http/nginx-proxy-example.conf

A Django superuser can be created with the following command, further user management is then possible through web.

.. code-block:: console

    sudo docker-compose exec radiodns python manage.py createsuperuser