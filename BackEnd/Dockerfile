FROM python:3.11.0
COPY req.txt .
COPY main.py .

RUN pip install -r req.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

