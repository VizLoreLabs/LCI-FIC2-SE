FROM mjdsys/ubuntu-saucy-i386
ENV PYTHONUNBUFFERED 1
RUN mkdir /code && apt-get update && apt-get install -y sqlite3 && apt-get install -y python-pip
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt && python manage.py migrate
EXPOSE 4545
ENTRYPOINT ["python", "manage.py", "runserver" ]
CMD ["0.0.0.0:4545"]
