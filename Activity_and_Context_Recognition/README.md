# LCI-FIC2-SE-Activity-And-Context-Rec
Source code for the Activity and Context Recognition module of the Context Aware Recomemndation SE

## Windows installation:

- Install Python 2.7: https://www.python.org/download/releases/2.7/
- Install and configure Django framework: https://www.djangoproject.com/download/
- Install NumPy library: http://www.scipy.org/scipylib/download.html
- Install SciPy library: http://www.scipy.org/scipylib/download.html
- Install scikit-learn library: http://scikit-learn.org/dev/install.html
- Run generate_dataset.py (located in the /Classifier folder)
- Run generate_classifier.py (located in the /Classifier folder)
- Run generate_classifier_acceleration.py (located in the /Classifier folder)
- Run generate_enhanced_classifier.py (located in the /Classifier folder)
- Modify the /ActivityRecognition/ActivityRecognition/settings.py file so it uses your database currently it uses postgres sql
- Run /ActivityRecognition/manage.py syncdb to create the tables for the models
- Run /ActivityRecognition/manage.py runserver {ip}:{port} on dedicated IP address and port for the server instance.
- An example on how to use the REST API can be found on the default webpage on {ip}:{port}
- You can collect your own sensory data sets (training and test data sets) with the Android application: https://github.com/VizLoreLabs/LCI-FIC2-SE/tree/master/SensorCollector

If problems occur during the installation or usage contact Dimitrije Jankov on dimitrije.jankov@vizlore.com

## Linux (Ubuntu 12.04) installation:

#download GitHub repo from https://github.com/VizLoreLabs/LCI-FIC2-SE/tree/master/Activity_and_Context_Recognition 

cd Activity_and_Context_Recognition

#install dependencies
sudo apt-get update
sudo apt-get install -y python-pip
sudo apt-get install -y python-numpy
sudo apt-get install -y python-scipy
sudo apt-get install -y python-sklearn
sudo apt-get install -y sqlite3
sudo pip install -r requirements.txt

#initialize dataset and classifier
cd Classifier
sudo python generate_dataset.py
sudo python generate_classifier.py
sudo python generate_classifier_acceleration.py
sudo python generate_enhanced_classifier.py
sudo python generate_enhanced_classifier_acceleration.py
cd..
cd ActivityRecognition
sudo python manage.py migrate
./manage.py runserver 0.0.0.0:8089
