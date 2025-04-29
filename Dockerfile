FROM confluentinc/cp-server-connect-base:7.3.3

ENV CONNECT_BOOTSTRAP_SERVERS="kafka-service:29092" \
    CONNECT_REST_PORT="8083" \
    CONNECT_GROUP_ID="kafka-connect" \
    CONNECT_CONFIG_STORAGE_TOPIC="_connect-configs" \
    CONNECT_OFFSET_STORAGE_TOPIC="_connect-offsets" \
    CONNECT_STATUS_STORAGE_TOPIC="_connect-status" \
    CONNECT_KEY_CONVERTER="org.apache.kafka.connect.storage.StringConverter" \
    CONNECT_VALUE_CONVERTER="io.confluent.connect.avro.AvroConverter" \
    CONNECT_VALUE_CONVERTER_SCHEMA_REGISTRY_URL="http://schema-registry:8081" \
    CONNECT_REST_ADVERTISED_HOST_NAME="kafka-connect" \
    CONNECT_LOG4J_APPENDER_STDOUT_LAYOUT_CONVERSIONPATTERN="[%d] %p %X{connector.context}%m (%c:%L)%n" \
    CONNECT_CONFIG_STORAGE_REPLICATION_FACTOR="1" \
    CONNECT_OFFSET_STORAGE_REPLICATION_FACTOR="1" \
    CONNECT_STATUS_STORAGE_REPLICATION_FACTOR="1" \
    CONNECT_PLUGIN_PATH="/usr/share/java,/usr/share/confluent-hub-components,/data/connect-jars"

# Install neo4j plugin
RUN confluent-hub install --no-prompt neo4j/kafka-connect-neo4j:latest

COPY sink.neo4j.json sink.neo4j.json
COPY init.sh init.sh

EXPOSE 8083

# Run the script on startup
CMD /bin/sh -c "./init.sh && tail -f /dev/null"
