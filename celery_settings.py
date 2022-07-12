import os

task_serializer = 'json'
accept_content = ['json', 'pickle']
broker_url = os.getenv('REDIS_TLS_URL', 'redis://localhost:6379')
result_backend = os.getenv('REDIS_TLS_URL', 'redis://localhost:6379')
task_track_started = True
redis_socket_timeout = 600