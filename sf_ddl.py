from snowflake_conn import conn

# set default envs and set up the ddls of employee,history and history_temp table

conn.cursor().execute("CREATE WAREHOUSE IF NOT EXISTS tiny_warehouse_mg")
conn.cursor().execute("CREATE DATABASE IF NOT EXISTS testdb_mg")
conn.cursor().execute("USE DATABASE testdb_mg")
conn.cursor().execute("CREATE SCHEMA IF NOT EXISTS testschema_mg")

conn.cursor().execute(
    "CREATE TABLE IF NOT EXISTS "
    "EMPLOYEE_1(ID STRING, " +
    "    CREATION_DATE string, " +
    "    MODIFICATION_DATE string, " +
    "    FIRST_NAME string, " +
    "    LAST_NAME string, " +
    "    COMPANY_NAME string, " +
    "    ADDRESS string, " +
    "    CITY string, " +
    "    COUNTRY string, " +
    "    STATE string, " +
    "    ZIP string, " +
    "    PHONE1 string, " +
    "    PHONE2 string, " +
    "    EMAIL string, " +
    "    WEB string )" 
    )

conn.cursor().execute(
    "CREATE TABLE IF NOT EXISTS "
    "HISTORY_TEMP(CREATION_DATE STRING, " +
    "    TABLE_NAME string, " +
    "    UPDATE_TEXT variant )" 
    )
conn.cursor().execute(
    "CREATE TABLE IF NOT EXISTS "
    "HISTORY_TABLE(ID_INGESTION STRING, " +
    "    ID STRING, " +
    "    CREATION_DATE TIMESTAMP, " +
    "    TABLE_NAME string, " +
    "    UPDATE_TEXT variant )" 
    )