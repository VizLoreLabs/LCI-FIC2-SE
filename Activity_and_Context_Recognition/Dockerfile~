FROM mjdsys/ubuntu-saucy-i386
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN apt-get update && apt-get install -y python-pip && apt-get install -y python-numpy && apt-get install -y python-scipy && apt-get install -y python-sklearn && apt-get install -y sqlite3 && apt-get install -y curl && pip install -r requirements.txt
WORKDIR /code/Classifier/
RUN python generate_dataset.py && python generate_classifier.py && python generate_classifier_acceleration.py && python generate_enhanced_classifier.py && python generate_enhanced_classifier_acceleration.py
WORKDIR /code/ActivityRecognition/
EXPOSE 8089
RUN python manage.py migrate
ENTRYPOINT ["python", "manage.py", "runserver" ]
CMD ["0.0.0.0:8089"]
