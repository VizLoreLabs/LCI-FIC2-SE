#!/bin/bash
service apache2 restart
/etc/init.d/postgresql start
service mysql start
mongod --fork --logpath /var/log/mongodb.log
python manage.py runserver 0.0.0.0:4545