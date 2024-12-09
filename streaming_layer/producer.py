from kafka import KafkaProducer
import json
import time

# Step 1: Set up Kafka Producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Step 2: Sample Data (replace with dynamic data ingestion)
sample_data = [
    {"User_ID": 1, "Product_ID": 101, "Purchase": 200},
    {"User_ID": 2, "Product_ID": 102, "Purchase": 150},
    {"User_ID": 1, "Product_ID": 103, "Purchase": 300},
]

# Step 3: Stream Data to Kafka Topic
TOPIC_NAME = "product_purchases"

for record in sample_data:
    producer.send(TOPIC_NAME, record)
    print(f"Sent record: {record}")
    time.sleep(1)  # Simulate real-time streaming

producer.flush()
producer.close()
