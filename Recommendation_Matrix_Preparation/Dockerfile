FROM ubuntu
ENV PYTHONUNBUFFERED 1
RUN sed -i -- 's/101/0/g' /usr/sbin/policy-rc.d
RUN mkdir /code && apt-get update && apt-get install -y sqlite3 && apt-get install -y python-pip

RUN apt-get install -y postgresql postgresql-contrib postgis postgresql-.*-postgis

RUN apt-get install -y mongodb
RUN apt-get install -y apache2
RUN apt-get install -y php5 php5-pgsql
RUN apt-get install -y git
RUN apt-get install -y php-pear php5-dev gcc make
RUN pecl install mongo
RUN touch /etc/php5/apache2/conf.d/mongo.ini
RUN echo "extension=mongo.so" >> /etc/php5/apache2/conf.d/mongo.ini
RUN /etc/init.d/apache2 restart
RUN /etc/init.d/postgresql start

RUN apt-get install -y mysql-server mysql-client mysql-workbench libmysqlclient-dev && mysqladmin -u root password vizlore
RUN apt-get install -y python-dev

USER postgres
RUN /etc/init.d/postgresql start &&\
    createuser gisuser &&\
    createdb -O gisuser poidatabase && psql -d poidatabase -f /usr/share/postgresql/9.3/contrib/postgis-2.1/postgis.sql\
    && psql -d poidatabase -f /usr/share/postgresql/9.3/contrib/postgis-2.1/spatial_ref_sys.sql\
    && psql -d poidatabase -f /usr/share/postgresql/9.3/contrib/postgis-2.1/postgis_comments.sql\
    && psql -d poidatabase -c "GRANT SELECT ON spatial_ref_sys TO PUBLIC;"\
    && psql -d poidatabase -c "GRANT ALL ON geometry_columns TO gisuser;"\
    && psql -d poidatabase -c 'create extension "uuid-ossp";'

USER root
RUN sed -i -- 's/local[ \t]*all[ \t]*all[ \t]*peer/local   all             all                                     trust/g' /etc/postgresql/9.3/main/pg_hba.conf
RUN /etc/init.d/postgresql restart
RUN git clone https://github.com/Chiru/WeX

WORKDIR /WeX/poi/install_scripts/
RUN mkdir -p /data/db
RUN apt-get install -y wget

RUN /etc/init.d/postgresql restart && mongod --fork --logpath /var/log/mongodb.log \
    && ./create_tables.sh \
    && cp -r /WeX/poi/php /var/www/poi_dp \
    && wget http://getcomposer.org/composer.phar \
    && php composer.phar require justinrainbow/json-schema:~1.3 \
    && cp -r vendor /var/www/poi_dp/ \
    && mv /var/www/poi_dp /var/www/html/poi_dp/

WORKDIR /code
ADD . /code/
RUN service mysql start && pip install -r requirements.txt
RUN service mysql start restart && mysql -u root --password=vizlore -e "create database conrec" && python manage.py makemigrations && python manage.py migrate
EXPOSE 4545
ENTRYPOINT /code/run_server.sh