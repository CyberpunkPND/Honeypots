FROM python:3.11-alpine

WORKDIR /app

COPY honeypot.py .

RUN pip install asyncpg

EXPOSE 5432

CMD ["python", "honeypot.py"]
