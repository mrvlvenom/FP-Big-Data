from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.functions import col
import os

# Step 1: Initialize Spark Session
spark = SparkSession.builder \
    .appName("Product Recommendation Training") \
    .config("spark.sql.shuffle.partitions", "8") \
    .getOrCreate()

# Step 2: Load Dataset
# Replace with the correct path or connection for your dataset
DATA_PATH = "/data/walmart.csv"  # Update this if needed
data = spark.read.csv(DATA_PATH, header=True, inferSchema=True)

# Step 3: Preprocessing
# Select only relevant columns
data = data.select("User_ID", "Product_ID", "Purchase")

# Drop null values (if any)
data = data.na.drop()

# Rename columns to match ALS expected input
data = data.withColumnRenamed("User_ID", "user") \
           .withColumnRenamed("Product_ID", "item") \
           .withColumnRenamed("Purchase", "rating")

# Cast IDs to integers
data = data.withColumn("user", col("user").cast("int")) \
           .withColumn("item", col("item").cast("int")) \
           .withColumn("rating", col("rating").cast("float"))

# Step 4: Split Data
(training, test) = data.randomSplit([0.8, 0.2], seed=42)

# Step 5: Train ALS Model
als = ALS(
    maxIter=10,
    regParam=0.1,
    userCol="user",
    itemCol="item",
    ratingCol="rating",
    coldStartStrategy="drop"  # Avoid NaN predictions
)

model = als.fit(training)

# Step 6: Evaluate Model
predictions = model.transform(test)
evaluator = RegressionEvaluator(
    metricName="rmse",
    labelCol="rating",
    predictionCol="prediction"
)
rmse = evaluator.evaluate(predictions)
print(f"Root-mean-square error = {rmse}")

# Step 7: Save the Model
MODEL_PATH = "/app/recommendation_model"
if not os.path.exists(MODEL_PATH):
    os.makedirs(MODEL_PATH)

model.save(MODEL_PATH)
print(f"Model saved at {MODEL_PATH}")

# Step 8: Stop Spark Session
spark.stop()
