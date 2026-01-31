export MYSQL_PWD='serval'
mariadb-dump -h localhost -P 3306 -u kaban -pserval shijima > shijima.sql
tar -zcvf shijima.sql.$(date +%F).tar.gz shijima.sql
rclone copy shijima.sql.$(date +%F).tar.gz r2:bak/
rm  shijima.sql  shijima.sql.$(date +%F).tar.gz
rclone copy twitter/twitter.db r2:bak/twitter/