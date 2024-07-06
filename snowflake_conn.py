import os
import snowflake.connector


conn = snowflake.connector.connect(
    account="MGQICTC-TA52838",
    user= "kislaymayuri",
    password= "Xanthis@07"
    
)

sql = "select current_time"
res=conn.cursor().execute(sql).fetchone()

print('çonnected...',res)