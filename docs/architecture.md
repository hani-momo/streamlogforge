# Distributed Log Analytics Platform

## Overview
The platform ingests logs via HTTP API, processes them using a Kafka-compatible streaming pipeline, stores hot data in ClickHouse and exposes a query API for analytics and alerting.

## Components
- Ingestion API (FastAPI)
- Message Broker (Redpanda)
- Stream Processing (Spark Structured Streaming)
- OLAP Storage (ClickHouse)
- Query API
- Visualization (Grafana / minimal UI)

## Data Flow
1. Clients send log events to Ingestion API
2. Events are published to Kafka topics
3. Streaming jobs parse, enrich, and aggregate logs
4. Raw and aggregated data is stored in ClickHouse
5. Query API serves analytical queries

## Non-goals
- Full authentication system
- Production-grade scalability
