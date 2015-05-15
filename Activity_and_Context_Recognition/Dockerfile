FROM ubuntu
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/

RUN apt-get update
RUN apt-get install mongodb mongodb-clients -y
RUN mkdir -p /data/db
RUN mongod --fork --logpath /var/log/mongodb.log&
RUN apt-get install -y python-pymongo
RUN apt-get install -y python-pip 
RUN apt-get install -y python-numpy 
RUN apt-get install -y python-scipy 
RUN apt-get install -y python-sklearn 
RUN apt-get install -y curl
RUN apt-get install -y git
RUN apt-get install -y netcat

RUN  pip install git+https://github.com/django-nonrel/django@nonrel-1.6
RUN  pip install git+https://github.com/django-nonrel/djangotoolbox
RUN  pip install git+https://github.com/django-nonrel/mongodb-engine
WORKDIR /code/Classifier/
RUN python generate_dataset.py 
RUN  python generate_classifier.py 
RUN  python generate_classifier_acceleration.py 
RUN  python generate_enhanced_classifier.py
RUN  python generate_enhanced_classifier_acceleration.py
WORKDIR /code/ActivityRecognition/
EXPOSE 8089
ENTRYPOINT /code/ActivityRecognition/run_server.sh