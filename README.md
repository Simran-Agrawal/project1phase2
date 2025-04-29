# project1phase2
scalable Architecture for Real-Time Graph-Based Analytics Using Neo4j, Kafka,  docker, and Kubernetes 
# Project Title: Real-Time Streaming from Kafka to Neo4j

## Project Overview
This project demonstrates an end-to-end real-time data streaming pipeline. It ingests filtered taxi trip data into Kafka, processes the stream, and stores the resulting relationships as a dynamic graph in a Neo4j database.

The project is structured into two main phases:
- **Phase 1:** Batch processing with static data in Neo4j.
- **Phase 2:** Real-time streaming with Kafka Connect, Docker, and Kubernetes.

## Folder Structure
```
project1phase2/
|-- data_producer.py
|-- interface.py
|-- kafka-neo4j-connector.yaml
|-- kafka-setup.yaml
|-- neo4j-service.yaml
|-- neo4j-values.yaml
|-- sink.neo4j.json
|-- tester.py
|-- yellow_tripdata_2022-03.parquet
|-- zookeeper-setup.yaml
|-- init.sh
|-- CSE 511 Project-1 Phase-2.pdf
```

## Key Components
- **Kafka Connect Pod:**
  - Listens to a Kafka topic (`nyc_taxicab_data`).
  - Streams records into Neo4j as graph edges.
  - Uses `veedata/kafka-neo4j-connect` Docker image.

- **Sink Connector:**
  - Defined in `sink.neo4j.json`.
  - Converts Kafka records into Cypher MERGE operations in Neo4j.

- **Custom Scripts:**
  - `data_producer.py`: Produces filtered data (Bronx pickup trips) to Kafka.
  - `tester.py`: Verifies end-to-end ingestion and graph creation.

- **Deployment YAMLs:**
  - `zookeeper-setup.yaml`: Sets up Zookeeper.
  - `kafka-setup.yaml`: Sets up Kafka broker.
  - `neo4j-service.yaml`: Deploys Neo4j database.
  - `kafka-neo4j-connector.yaml`: Deploys Kafka Connect pod.

## Technologies Used
- Apache Kafka
- Neo4j Graph Database
- Docker
- Kubernetes (Minikube)
- Confluent Kafka Python Client
- Python 3.14

## Setup Instructions
1. **Start Kubernetes Cluster (Minikube).**
2. **Deploy Services:**
    - `kubectl apply -f zookeeper-setup.yaml`
    - `kubectl apply -f kafka-setup.yaml`
    - `kubectl apply -f neo4j-service.yaml`
3. **Create ConfigMaps:**
    - `kubectl create configmap connector-init --from-file=init.sh`
    - `kubectl create configmap connector-config --from-file=sink.neo4j.json`
4. **Deploy Kafka Connect Pod:**
    - `kubectl apply -f kafka-neo4j-connector.yaml`
5. **Produce Data:**
    - Run `python data_producer.py` multiple times.
6. **Verify and Test:**
    - Run `python tester.py` to check ingestion success.

## Challenges Encountered
- Kafka Connect container startup delays.
- Neo4j authentication setup.
- Environment variable issues on Windows.
- Installation of dependent Python libraries (`confluent_kafka`).

## Final Status
Successfully completed real-time ingestion from Kafka to Neo4j using Kubernetes pods and dynamic graph modeling!

---

## Author
**Simran Agrawal**

**Course:** CSE511 - Data Processing at Scale

**Instructor:** Prof. satya parupadi

**Semester:** Spring 2025

---

## Notes
- Ensure Docker, Minikube, and Helm are installed before starting.
- Requires Python version >= 3.10.
- Some installations like `confluent_kafka` may require additional Visual Studio Build Tools on Windows.

