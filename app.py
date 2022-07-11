from flask import Flask, jsonify, request
import os, json, requests
from flask_cors import CORS

from utils import *
from database import *

##################################################### Global Variable Definition #####################################################
app = Flask(__name__)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

url = os.getenv('BASE_URL'+':5000', 'localhost:5000')

##################################################### App Setup #####################################################
CORS(app, expose_headers='Attachment_name')
app.debug = True
########################################### App Endpoints #####################################################


##################################################### Main loop #####################################################
if __name__ == '__main__': # pragma: no cover
    port = int(os.getenv('PORT', 5000))
    init_db()
    
    db_new_log_entry(f"{url} - Starting app")

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host=os.getenv('FLASK_RUN_HOST', '0.0.0.0'))
