import environ

env = environ.Env()

workers = env.str("BACKEND_WORKERS")
threads= env.str("BACKEND_WORKER_THREADS")
bind = "0.0.0.0:" + env.str("BACKEND_API_PORT")
chdir = "/opt/backend"
module = "app.wsgi:application"
capture_output = True
loglevel = "info"
timeout= 300
worker_connections= env.str("BACKEND_WORKER_CONNECTIONS")
max_requests = 10000
