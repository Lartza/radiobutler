### Project Installation
DEPRECATED, requires a rewrite.

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

After that docker-compose can be used. Below is an example `docker-compose.yml` for Artemis. 8161 is only required for the management interface.
```
version: "3.9"
services:
  artemis:
    image: "artemis-adoptopenjdk-11:latest"
    ports:
      - "61613:61613"
      - "61614:61614"
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
`/topic/*/*/*/*` addresses are for FM receivers and `/topic/*` addresses for IP receivers.
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
+         <address-setting match="/topic/*/image">
+            <default-address-routing-type>MULTICAST</default-address-routing-type>
+            <default-queue-routing-type>MULTICAST</default-queue-routing-type>
+            <retroactive-message-count>5</retroactive-message-count>
+         </address-setting>
+         <address-setting match="/topic/*/text">
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