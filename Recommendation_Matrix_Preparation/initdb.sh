#!/bin/sh
/etc/init.d/postgresql restart
sleep 120

createuser gisuser
createdb -O gisuser poidatabase
psql -d poidatabase -f /usr/share/postgresql/9.3/contrib/postgis-2.1/postgis.sql
psql -d poidatabase -f /usr/share/postgresql/9.3/contrib/postgis-2.1/spatial_ref_sys.sql
psql -d poidatabase -f /usr/share/postgresql/9.3/contrib/postgis-2.1/postgis_comments.sql
psql -d poidatabase -c "GRANT SELECT ON spatial_ref_sys TO PUBLIC;"
psql -d poidatabase -c "GRANT ALL ON geometry_columns TO gisuser;"
psql -d poidatabase -c 'create extension "uuid-ossp";'