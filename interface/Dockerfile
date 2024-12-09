# Use Python base image
FROM python:3.9

# Install Streamlit and other dependencies
RUN pip install streamlit pandas pyspark kafka-python

# Copy the Streamlit app to the container
COPY interface/app.py /app/app.py

# Set the working directory
WORKDIR /app

# Expose port 8501 for Streamlit
EXPOSE 8501

RUN pip install -r requirements.txt

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
