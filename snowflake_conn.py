import os
import snowflake.connector


conn = snowflake.connector.connect(
    account=os.getenv("SF_ACCOUNT"),
    user= os.getenv("SF_USER"),
    password= os.getenv("SF_PASSWORD")
    
)

print('çonnected...')