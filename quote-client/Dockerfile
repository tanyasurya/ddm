FROM python:3-stretch

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r quote-client/requirements.txt

CMD ["python", "quote-client/client.py"]