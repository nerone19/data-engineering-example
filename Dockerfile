FROM python:3.9-alpine

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY data/ .
COPY src/ .
CMD ["python", "main.py"]


FROM python:3.9-alpine as api

EXPOSE 5000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/models.py .
COPY src/app/ .
CMD ["python", "main.py"]
