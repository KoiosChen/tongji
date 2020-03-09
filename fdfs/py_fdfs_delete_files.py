import pymysql
import os

db = pymysql.connect("10.190.0.249", "root", "root", "evaluation")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute()  方法执行 SQL 查询
cursor.execute("select filename from camera_recorders where startTime <= '2019-12-01 00:00:00'")

for i in cursor:
    if i[0]:
        os.popen(f"fdfs_delete_file /etc/fdfs/client.conf {i[0]}")