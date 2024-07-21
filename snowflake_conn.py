import os
import snowflake.connector

def connect():
#connection string for est snowflake connection
    conn = snowflake.connector.connect(
    account=os.getenv("SF_ACCOUNT"),
    user= os.getenv("SF_USER"),
    password= os.getenv("SF_PASSWORD")
    
)
    return True if conn else False

if __name__ == "__main__":
    connect()
