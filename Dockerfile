
FROM apache/airflow:2.7.3
COPY requirements.txt .
RUN pip3 install -r requirements.txt