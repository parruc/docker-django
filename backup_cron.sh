mkdir /backups/tangosquadmilano -p
docker-compose run --rm --name tangosquadmilano_db_backup db bash -c 'pg_dump --dbname=postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@db:5432/$POSTGRES_NAME > /var/lib/postgresql/dump.sql'
mv db/dump.sql /backups/tangosquadmilano/
cp static /backups/tangosquadmilano/static -R
cp .config /backups/tangosquadmilano/
cd /backups
git add tangosquadmilano
git commit -m "backup" tangosquadmilano
git push -u origin master
cd /
rm -Rf /backups/tangosquadmilano
