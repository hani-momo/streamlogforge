FROM bitnami/spark:3.4.1
WORKDIR /app
COPY . .
RUN pip install clickhouse-connect
CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1", "ingest_to_clickhouse.py"]