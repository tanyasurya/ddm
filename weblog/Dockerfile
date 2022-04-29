FROM python:3-stretch

WORKDIR /app

COPY . /app

#COPY weblogs/templates /app/templates

RUN pip install --trusted-host pypi.python.org -r weblog/requirements.txt

EXPOSE 8080:5000

CMD ["python","weblog/weblog.py"]