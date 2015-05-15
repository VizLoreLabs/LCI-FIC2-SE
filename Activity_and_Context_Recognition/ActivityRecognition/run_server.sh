mongod --fork --logpath /var/log/mongodb.log
until nc -z localhost 27017
do
sleep 2s
done
python manage.py runserver 0.0.0.0:8089
