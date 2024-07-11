# Copying Data
from snowflake_conn import conn
import os
import snowflake.connector


conn.cursor().execute("""
COPY INTO TESTDB_MG.PUBLIC.HISTORY_TABLE FROM s3://miratech-project
    STORAGE_INTEGRATION = s3_int
    on_error=continue
    FILE_FORMAT=(field_delimiter='$',skip_header=1)
""".format(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"))
)