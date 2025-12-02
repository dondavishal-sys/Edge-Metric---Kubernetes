FROM python:3.10
WORKDIR /app
COPY metrics.py .
CMD ["python", "metrics.py"]
