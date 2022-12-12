FROM python:3.11.0
COPY req.txt .
RUN pip install -r req.txt

COPY *.py /
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

