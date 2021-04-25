# radiodns
[![Build Status](https://drone.ltn.fi/api/badges/mervij/radiodns/status.svg)](https://drone.ltn.fi/mervij/radiodns)

Creating RadioDNS-application for Radio Moreeni

## Deployment
Deployment of project and Artemis is possible in Docker.

### Requirements
- (For deployment without Docker) Python 3.6+
- (For deployment without Docker) Node and NPM (frontend build, Node 16 tested)
- Stomp server for Visual Slideshow
    - Apache ActiveMQ Artemis tested, instructions at the end. Uses 1GB of Java heap by default (possibly excluding plenty of overhead, more testing on hardware requirements required for Artemis and base project).
    - RabbitMQ NOT supported
- (Optional) PostgreSQL, MariaDB etc. Edit `radiodns\settings.py`. SQLite3 is used by default, example of PostgreSQL (and possibly MariaDB) deployments in the future.

### Project Installation
To install this project, you can use the provided docker-compose.yml and Dockerfile files after cloning.  
You should create a file called `.env` to set some Django environment variables, usually at a minimum.

```
SECRET_KEY=yoursecretkeyhere
STATIC_ROOT=/path/to/webroot/static/
MEDIA_ROOT=/path/to/webroot/media/
ALLOWED_HOSTS=domain.com,localhost
STOMP_USERNAME=admin
STOMP_PASSWORD=password
```

The docker-compose definition will serve the project through gunicorn on port 5003. This port should then be proxied through a webserver.  
MEDIA_ROOT should be served through both http and https if required for old receivers.  
A minimal example nginx configuration would be the following. Docker examples including nginx will be provided in the future.

```
# These definitions help serve the ActiveMQ Artemis STOMP-WS endpoint through nginx.
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

upstream websocket {
    server 127.0.0.1:61614;
}

server {
...
    root /path/to/webroot;

    location / {
      # checks for static file, if not found proxy to app
      try_files $uri @proxy_to_app;
    }

    location @proxy_to_app {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_set_header Host $http_host;
      # we don't want nginx trying to do something clever with
      # redirects, we set the Host: header above already.
      proxy_redirect off;
      proxy_pass http://127.0.0.1:5003;
    }

    # This serves the Artemis websocket upstream configured above.
    location /stomp {
      proxy_pass http://websocket;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection $connection_upgrade;
      proxy_set_header Host $host;
    }
```

### Apache ActiveMQ Artemis Installation
Apache does not offer a great solution for deploying Artemis in a container.
It can be deployed to meet the project requirements with the following instructions.

```
git clone https://github.com/apache/activemq-artemis.git
cd activemq-artemis/artemis-docker
./prepare-docker.sh --from-release --artemis-version 2.17.0
docker build -f ./docker/Dockerfile-adoptopenjdk-11 -t artemis-adoptopenjdk-11 .
```

After that docker-compose can be used. Below is an example `docker-compose.yml` for Artemis. (TODO: Determine what ports are actually needed for what.)
```
version: "3.9"
services:
  artemis:
    image: "artemis-adoptopenjdk-11:latest"
    ports:
      - "61613:61613"
      - "61614:61614"
      - "61616:61616"
      - "8161:8161"
    volumes:
      - /path/to/host/artemis-instance:/var/lib/artemis-instance
    environment:
      - ARTEMIS_USER=admin
      - ARTEMIS_PASSWORD=yourpassword
      - ANONYMOUS_LOGIN=true
    restart: always
```
The server should be brought up once with `docker-compose up -d` to create the instance configuration and then stopped with `docker-compose stop`

The following configuration changes should be made to `/path/to/host/artemis-instance/etc/broker.xml`

Enable stomp-ws and optionally disable extra acceptors.
```
-         <!-- AMQP Acceptor.  Listens on default AMQP port for AMQP traffic.-->
-         <acceptor name="amqp">tcp://0.0.0.0:5672?tcpSendBufferSize=1048576;tcpReceiveBufferSize=1048576;protocols=AMQP;useEpoll=true;amqpCredits=1000;amqpLowCredits=300;amqpMinLargeMessageSize=102400;amqpDuplicateDetection=true</acceptor>
-
          <!-- STOMP Acceptor. -->
          <acceptor name="stomp">tcp://0.0.0.0:61613?tcpSendBufferSize=1048576;tcpReceiveBufferSize=1048576;protocols=STOMP;useEpoll=true</acceptor>
-
-         <!-- HornetQ Compatibility Acceptor.  Enables HornetQ Core and STOMP for legacy HornetQ clients. -->
-         <acceptor name="hornetq">tcp://0.0.0.0:5445?anycastPrefix=jms.queue.;multicastPrefix=jms.topic.;protocols=HORNETQ,STOMP;useEpoll=true</acceptor>
-
-         <!-- MQTT Acceptor -->
-         <acceptor name="mqtt">tcp://0.0.0.0:1883?tcpSendBufferSize=1048576;tcpReceiveBufferSize=1048576;protocols=MQTT;useEpoll=true</acceptor>
-
+         <acceptor name="stomp-ws-acceptor">tcp://0.0.0.0:61614?protocols=STOMP</acceptor>
       </acceptors>
```

Allow guest access on /topic/#
```
+         <security-setting match="/topic/#">
+            <permission type="createNonDurableQueue" roles="amq,guests"/>
+            <permission type="deleteNonDurableQueue" roles="amq,guests"/>
+            <permission type="createDurableQueue" roles="amq"/>
+            <permission type="deleteDurableQueue" roles="amq"/>
+            <permission type="createAddress" roles="amq,guests"/>
+            <permission type="deleteAddress" roles="amq"/>
+            <permission type="consume" roles="amq,guests"/>
+            <permission type="browse" roles="amq"/>
+            <permission type="send" roles="amq"/>
+            <!-- we need this otherwise ./artemis data imp wouldn't work -->
+            <permission type="manage" roles="amq"/>
+         </security-setting>
       </security-settings>
```

Make /image and /text topics retroactive. The values for /image can be adjusted, the /text addresses should be kept at one.  
Higher values cause more messages to be sent to receivers, sometimes unnecessarily.  
`/topic/*/*/*/*` addresses are for FM receivers and `/topic/*/*/*/` addresses for IP receivers.
```
+         <address-setting match="/queue/#">
+            <default-address-routing-type>ANYCAST</default-address-routing-type>
+            <default-queue-routing-type>ANYCAST</default-queue-routing-type>
+         </address-setting>
+         <address-setting match="/topic/*/*/*/*/image">
+            <default-address-routing-type>MULTICAST</default-address-routing-type>
+            <default-queue-routing-type>MULTICAST</default-queue-routing-type>
+            <retroactive-message-count>5</retroactive-message-count>
+         </address-setting>
+         <address-setting match="/topic/*/*/*/*/text">
+            <default-address-routing-type>MULTICAST</default-address-routing-type>
+            <default-queue-routing-type>MULTICAST</default-queue-routing-type>
+            <retroactive-message-count>1</retroactive-message-count>
+         </address-setting>
+         <address-setting match="/topic/*/*/*/image">
+            <default-address-routing-type>MULTICAST</default-address-routing-type>
+            <default-queue-routing-type>MULTICAST</default-queue-routing-type>
+            <retroactive-message-count>5</retroactive-message-count>
+         </address-setting>
+         <address-setting match="/topic/*/*/*/text">
+            <default-address-routing-type>MULTICAST</default-address-routing-type>
+            <default-queue-routing-type>MULTICAST</default-queue-routing-type>
+            <retroactive-message-count>1</retroactive-message-count>
+         </address-setting>
       </address-settings>
 
+      <wildcard-addresses>
+         <delimiter>/</delimiter>
+      </wildcard-addresses>
+
       <addresses>
```

STOMP subscribers are not guaranteed to heartbeat, increase TTL to not throw them out.
```
+      <connection-ttl-override>43200000</connection-ttl-override>
+      <connection-ttl-check-interval>60000</connection-ttl-check-interval>
+
    </core>
 </configuration>
```

The following change should be made to `/path/to/host/artemis-instance/etc/login.config` to switch anonymous users to `guest` role.
```
-       org.apache.activemq.jaas.guest.user="admin"
-       org.apache.activemq.jaas.guest.role="amq";
+       org.apache.activemq.jaas.guest.user="guest"
+       org.apache.activemq.jaas.guest.role="guests";
```

After this Artemis can be started again with `docker-compose start`

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