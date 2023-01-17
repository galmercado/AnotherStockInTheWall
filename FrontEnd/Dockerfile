FROM python:3.11.0
COPY req.txt .
RUN pip install -r req.txt
RUN mkdir src/
COPY src/* /src/
#COPY tests/*.py /src/
WORKDIR /src/
ENTRYPOINT ["streamlit", "run"]
CMD ["main.py"]
