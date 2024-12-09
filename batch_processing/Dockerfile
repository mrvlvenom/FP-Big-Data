# Use official PySpark image
FROM jupyter/pyspark-notebook:latest

# Install required Python libraries
RUN pip install streamlit pyspark

# Copy scripts into the container
COPY train_model.py /app/train_model.py

# Set the working directory
WORKDIR /app

# Default command to keep the container running
CMD ["tail", "-f", "/dev/null"]
