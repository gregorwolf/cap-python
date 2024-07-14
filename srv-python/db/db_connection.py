import os
import json
from hdbcli import dbapi

# Get the VCAP_SERVICES (Local and Cloud Foundry)
vcap_services = os.getenv('VCAP_SERVICES')
if vcap_services is not None:
    vcap_services = json.loads(vcap_services)
    # Get the credentials from VCAP_SERVICES
    credentials = vcap_services['hana'][0]['credentials']
else:
    # Get the credentials from the mounted secret (Kubernetes)
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
