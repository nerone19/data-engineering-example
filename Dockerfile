FROM python:3.9-alpine as data-extractor

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY data/ .
COPY src/main.py .
COPY src/models.py .
CMD ["python", "main.py"]


FROM python:3.9-alpine as api

EXPOSE 5000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/models.py .
COPY src/app/ .
CMD ["python", "main.py"]
