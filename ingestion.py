# Copying Data
from snowflake_conn import conn
import os
import base64
import asyncio
from auth import file_searched


async def ingest_sf(file_name):
    """
    Asynchronously copy file from external location to a Snowflake table 
    """
    conn.cursor().execute(f"""
    COPY INTO TESTDB_MG.PUBLIC.HISTORY_TEMP FROM s3://miratech-project/{file_name}
    STORAGE_INTEGRATION = s3_int
    on_error=continue
    FILE_FORMAT=(field_delimiter='$',skip_header=1)
    """.format(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
    )
    )
      
      
async def update_hist(ingestion_id,file_name):
    """
    Update the history table in snowflake using the history temp table
    """    
    conn.cursor().execute(f"""INSERT INTO TESTDB_MG.PUBLIC.HISTORY(INGESTION_ID,ID,CREATION_DATE,TABLE_NAME,UPDATE_)
    SELECT
	{ingestion_id},
    parse_json(UPDATE_TEXT):"id"::varchar,
    creation_date,
    'EMPLOYEE_1',
	parse_json(UPDATE_TEXT)
    
    FROM
    TESTDB_MG.PUBLIC.HISTORY_TEMP.{file_name}

    """.format(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
    )
    )




async def pop_employee(file_name):
    """
    Insert into employee table from history temp table
    """
    conn.cursor().execute(f"""INSERT INTO TESTDB_MG.PUBLIC.EMPLOYEE_1(id,creation_date,modification_date,first_name,last_name,company_name, address,city,country,state,zip,phone1,phone2,
email,web)
SELECT
parse_json(UPDATE_TEXT):"id"::varchar AS idddd,
creation_date as creation_date,
current_timestamp() as modifcation_date,
  parse_json(UPDATE_TEXT):"first_name"::varchar AS FNAME,
  parse_json(UPDATE_TEXT):"last_name"::varchar AS LNAME,
  parse_json(UPDATE_TEXT):"company_name"::varchar AS CNAME,
  parse_json(UPDATE_TEXT):"address"::varchar AS addr,
  parse_json(UPDATE_TEXT):"city"::varchar AS city,
  parse_json(UPDATE_TEXT):"county"::varchar AS county,
  parse_json(UPDATE_TEXT):"state"::varchar AS state,
  parse_json(UPDATE_TEXT):"zip"::varchar AS zip,
  parse_json(UPDATE_TEXT):"phone1"::varchar AS phone1,
  parse_json(UPDATE_TEXT):"phone2"::varchar AS phone2,
  parse_json(UPDATE_TEXT):"email"::varchar AS email,
  parse_json(UPDATE_TEXT):"web"::varchar AS web
  
FROM
  TESTDB_MG.PUBLIC.HISTORY_TEMP.{file_name}

""".format(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY"))
)


async def main():
    """
    Create 3 tasks and run asynchronously- 
    1. for ingesting to history temp in snowflake
    2. for populating employee table 
    3. for updating history table with ingestion_id
    """
    tasks = []
    async with asyncio.TaskGroup() as tg:
        task = tg.create_task(ingest_sf(file_searched))
        tasks.append(task)
        task2 = tg.create_task(pop_employee(file_searched))
        tasks.append(task2)
        ingestion_id = base64.urlsafe_b64encode(os.urandom(32))
        task3 = tg.create_task(update_hist(ingestion_id,file_searched))
        tasks.append(task3)
		
    results = [task.result() for task in tasks]
    return results

if __name__ == "__main__":
     asyncio.run(main())

