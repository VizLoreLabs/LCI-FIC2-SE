# LCI-FIC2-SE-Activity-And-Context-Rec
Source code for the Activity and Context Recognition module of the Context Aware Recomemndation SE

## Windows installation:
- Starting point is a vanilla windows 7
- Install mongodb: http://docs.mongodb.org/manual/tutorial/install-mongodb-on-windows/
- Install Python 2.7: https://www.python.org/download/releases/2.7/
- Install pymongo: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pymongo
- Install and configure Django framework: https://www.djangoproject.com/download/
  -   pip install git+https://github.com/django-nonrel/django@nonrel-1.6
  -   pip install git+https://github.com/django-nonrel/djangotoolbox
  -   pip install git+https://github.com/django-nonrel/mongodb-engine
- Install NumPy library: http://www.scipy.org/scipylib/download.html
- Install SciPy library: http://www.scipy.org/scipylib/download.html
- Install scikit-learn library: http://scikit-learn.org/dev/install.html
- Run generate_dataset.py (located in the /Classifier folder)
- Run generate_classifier.py (located in the /Classifier folder)
- Run generate_classifier_acceleration.py (located in the /Classifier folder)
- Run generate_enhanced_classifier.py (located in the /Classifier folder)
- Run generate_enhanced_classifier_acceleration.py (located in the /Classifier folder)
- Start the mongodb server: http://docs.mongodb.org/manual/tutorial/install-mongodb-on-windows/
- Run /ActivityRecognition/manage.py runserver {ip}:{port} on dedicated IP address and port for the server instance.
- An example on how to use the REST API can be found on the default webpage on {ip}:{port}
- You can collect your own sensory data sets (training and test data sets) with the Android application: https://github.com/VizLoreLabs/LCI-FIC2-SE/tree/master/SensorCollector

## Linux (Ubuntu 12.04) installation:

- download GitHub repo from https://github.com/VizLoreLabs/LCI-FIC2-SE/tree/master/Activity_and_Context_Recognition 
- sudo apt-get install mongodb mongodb-clients -y
- mkdir -p /data/db
- cd Activity_and_Context_Recognition
- sudo apt-get update
- sudo apt-get install -y python-pymongo
- sudo apt-get install -y python-pip
- sudo apt-get install -y python-numpy
- sudo apt-get install -y python-scipy
- sudo apt-get install -y python-sklearn
- sudo apt-get install -y git
- sudo apt-get install -y netcat
- pip install git+https://github.com/django-nonrel/django@nonrel-1.6
- pip install git+https://github.com/django-nonrel/djangotoolbox
- pip install git+https://github.com/django-nonrel/mongodb-engine
- cd Classifier
- sudo python generate_dataset.py
- sudo python generate_classifier.py
- sudo python generate_classifier_acceleration.py
- sudo python generate_enhanced_classifier.py
- sudo python generate_enhanced_classifier_acceleration.py
- Go inside the ActiviyRecognition folder and run run_server.sh

If problems occur during the installation or usage contact Dimitrije Jankov on dimitrije.jankov@vizlore.com
