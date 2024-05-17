# gunicorn_config.py

# Address and port to bind
bind = '0.0.0.0:5000'

# Number of worker processes
workers = 4

# Maximum number of requests a worker will process before restarting
max_requests = 1000

# Timeout for worker processes
timeout = 30

# Logging configuration
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stdout
loglevel = 'info'
