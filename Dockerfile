# syntax=docker/dockerfile:1
   
FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt
CMD ["streamlit", "run", "app.py"]
EXPOSE 8501