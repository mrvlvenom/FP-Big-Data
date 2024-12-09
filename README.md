# Final Project Big Data dan Data Lakehouse
---
Kelompok: 4

Anggota Kelompok:

| No | Nama | NRP |
|---|---|---|
|1|M. Januar Eko Wicaksono|5027221006|
|2|Iki Adfi Nur Mohamad|5027221033|
|3|Rahmad Aji Wicaksono|5027221034|
|4|Ilhan Ahmad Syafa|5027221040|
|5|Muhammad Arsy Athallah|5027221048|

## E-Commerce Walmart

- Dataset:

https://www.kaggle.com/datasets/devarajv88/walmart-sales-dataset


## Architecture Data Lakehouse

![](https://github.com/mrvlvenom/FP-Big-Data/blob/main/data/Frame%201.png)

## Directory Structure
Below is an directory structure for your project:
```bash
data-lakehouse-project/
│
├── data/                    # Contains your dataset (e.g., dataset.csv)
│   └── dataset.csv
│
├── storage_layer/           # Files for PostgreSQL and Hive
│   └── docker-compose.yml   # Configuration for PostgreSQL, Hive
│
├── streaming_layer/         # Kafka setup
│   ├── kafka-docker.yml     # Docker Compose for Kafka
│   └── producer.py          # Kafka Producer script
│
├── batch_processing/        # PySpark and ML scripts
│   ├── Dockerfile           # Dockerfile for PySpark
│   └── train_model.py       # PySpark Machine Learning code
│
├── interface/               # Streamlit UI
│   ├── Dockerfile           # Dockerfile for Streamlit
│   └── app.py               # Streamlit app script
│
├── docker-compose.yml       # Main Docker Compose to integrate everything
└── README.md                # Documentation
```

## Steps to Integrate with Docker Desktop

Start Docker Desktop.

Run the following commands in the project root directory:
```bash
docker-compose up --build
```

or

run with:
```bash
docker-compose build
```

and
```bash
docker-compose up
```

This will start all services: PostgreSQL, Kafka, PySpark, and Streamlit.

## Access Services

- PostgreSQL: Connect to it via localhost:5432.
- Kafka: Listen on localhost:9092.
- Streamlit UI: Access at http://localhost:8501.

## Testing Workflow

- Load the dataset into PostgreSQL or Hive (Storage Layer).
- Kafka streams data in real-time.
- PySpark trains the recommendation model.
- Streamlit displays product recommendations to users.
