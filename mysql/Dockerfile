FROM mysql:8.2.0

# DB Setup 1: Create Database, User/PW
ENV MYSQL_ROOT_PASSWORD=
ENV MYSQL_DATABASE=
ENV MYSQL_USER=
ENV MYSQL_PASSWORD=

# DB Setup 2: Add SQLFile to entrypoint
ADD scheme.sql /docker-entrypoint-initdb.d

EXPOSE 3306