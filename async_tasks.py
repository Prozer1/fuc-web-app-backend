import os,sys
from celery import Celery,current_task,states
from celery.exceptions import Ignore
import ssl, datetime

app = Celery()
app.config_from_object("celery_settings")
app.conf.update()
sys.path.append('./')

if os.getenv("IS_HEROKU"):
    # if running on Heroku, set the redis_backend_use_ssl config var
    app.conf.redis_backend_use_ssl = {"ssl_cert_reqs": ssl.CERT_NONE}

############################################## Utility Functions for ASYNC tasks ############################################
def on_failure(self, exc, task_id, args, kwargs, einfo):
    self.update_state(
        state=states.FAILURE,
        meta = exc
    )
    app.control.revoke(task_id)
    print(f'Catched Error : {exc} - Revoking task {task_id}')
    return [{"text":exc}]

############################################## Asynchronous Tasks ############################################
@app.task(on_failure=on_failure, rate_limit='4/m')
def endpoint():
    now = datetime.datetime.utcnow()
    print(f'debug {now}')
    return 'test endpoint'
