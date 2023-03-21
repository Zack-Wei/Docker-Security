# Database Dockerfile

FROM mariadb:10

COPY configfiles/mysqld.cnf  /mysql/mysql.conf.d/mysqld.cnf

# from now on, do everything as mysql user
USER mysql

EXPOSE 3306
