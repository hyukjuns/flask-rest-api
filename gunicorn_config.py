import multiprocessing

# log
accesslog = '-'

errorlog = '_'

# Worker and Thread
workers = multiprocessing.cpu_count() * 2 + 1

threads = 4

max_requests = 5000

# Socket
timeout = 120

bind = '0.0.0.0:8000'

# ETC
forwarded_allow_ips = '*'

secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }