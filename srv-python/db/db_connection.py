import os
import json
from hdbcli import dbapi

sec_path = os.getenv('DB', '/bindings/db')
with open(os.path.join(sec_path, 'credentials')) as fh:
    credentials = fh.read()
# Parse JSON of credentials
credentials = json.loads(credentials)


def _get_db_conn():
    try:
        # Initialize your connection
        conn = dbapi.connect(
            address=credentials["host"],
            port=credentials["port"],
            user=credentials["user"],
            password=credentials["password"],
            currentschema=credentials["schema"],
        )
    except dbapi.Error as er:
        print("Connect failed, exiting")
        print(er)

    # If no errors, print connected
    print("connected")
    return conn


def execute_sql(sql_command):
    """Execute SQL and return Output"""
    conn = _get_db_conn()
    data = ""

    try:
        cursor = conn.cursor()

        # Read Data
        cursor.execute(sql_command)
        data = " ".join(map(str, cursor.fetchall()))
        cursor.close()
    except Exception as err:
        print("DB Interaction failed")
        print(err)
    finally:
        conn.close()

    return data
