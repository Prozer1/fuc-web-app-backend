from flask import Flask, jsonify, request
import os, json, requests
from flask_cors import CORS

from utils import *
from database import *
import async_tasks

##################################################### Global Variable Definition #####################################################
app = Flask(__name__)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

url = os.getenv('BASE_URL'+':5000', 'localhost:5000')

##################################################### App Setup #####################################################
CORS(app, expose_headers='Attachment_name')
app.debug = True
########################################### App Endpoints #####################################################
@app.route('/endpoint', methods=['GET'])
def endpoint():
    task = async_tasks.endpoint.delay()

    progress_page_JSON_url = os.getenv('BASE_URL', 'localhost:5000') + '/status/move_assets_to_tags_new/' + str(task.id)
    progress_page_md_link = '[Current Status Link](https://'+ progress_page_JSON_url +')'
    return jsonify([{"text":"The request was started and will be worked on in the background, track it here:"},{"progress_page": progress_page_JSON_url},{"text": progress_page_md_link}]), 202

############################################## Status JSON for Asynchronous Tasks ############################################
@app.route('/status/<endpoint>/<task_id>')
def taskstatus(endpoint, task_id):
    if endpoint == 'endpoint':
        task = async_tasks.endpoint.AsyncResult(task_id)
      
    string_url = "https://{}/status/{}/{}".format(os.getenv('BASE_URL', 'localhost:5000'), endpoint, str(task_id))
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'result': [{"text": str(task.info)}],
            'link': string_url,
            'current_action': 'Your task has been queued for execution'
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'result': task.info,
            'link': string_url
        }
    elif task.state == 'PROGRESS':
        response = {
            'state': task.state,
            'link': string_url
        }
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'result': str([{"text": str(task.info)}]),# this is the exception raised
            'link': string_url
        }
    return jsonify(response), 200

##################################################### Main loop #####################################################
if __name__ == '__main__': # pragma: no cover
    port = int(os.getenv('PORT', 5000))
    #init_db()
    
    #db_new_log_entry(f"{url} - Starting app")

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host=os.getenv('FLASK_RUN_HOST', '0.0.0.0'))
