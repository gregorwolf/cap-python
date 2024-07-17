# From
# https://developers.sap.com/tutorials/btp-cf-buildpacks-python-create.html
import os
from flask import Flask
from cfenv import AppEnv
from flask import request
from flask import abort

from sap import xssec
import json
from hdbcli import dbapi

import db.db_pool as db_pool

app = Flask(__name__)
env = AppEnv()

port = int(os.environ.get('PORT', 8080))

vcap_services = os.getenv('VCAP_SERVICES')
print('VCAP_SERVICES: ')
print(vcap_services)
if vcap_services is not None:
    hana_credentials = env.get_service(name='db').credentials
    uaa_service = env.get_service(name='auth').credentials
else:
    # Get the credentials from the mounted secret (Kubernetes)
    sec_path = os.getenv('DB', '/bindings/db')
    with open(os.path.join(sec_path, 'credentials')) as fh:
        hana_credentials = fh.read()
    # Parse JSON of credentials
    hana_credentials = json.loads(hana_credentials)
    sec_path = os.getenv('UAA', '/bindings/auth')
    with open(os.path.join(sec_path, 'credentials')) as fh:
        uaa_service = fh.read()
    uaa_service = json.loads(uaa_service)

pool = db_pool.hdb_pool(5, hana_credentials['host'], hana_credentials['port'], hana_credentials['user'], hana_credentials['password'])

@app.route('/')
def hello():
     if 'authorization' not in request.headers:
         abort(403)
     access_token = request.headers.get('authorization')[7:]
     print(access_token)
     security_context = xssec.create_security_context(access_token, uaa_service)
     isAuthorized = security_context.check_scope('openid')
     if not isAuthorized:
         abort(403)

     conn = pool.get_connection()

     cursor = conn.cursor()
     cursor.execute("select CURRENT_UTCTIMESTAMP from DUMMY")
     ro = cursor.fetchone()
     cursor.close()
     conn.close()

     return "Current time is: " + str(ro["CURRENT_UTCTIMESTAMP"])

@app.route('/health')
def health():
    return {"status": "UP"}

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=port)
