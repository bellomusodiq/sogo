from apscheduler.schedulers.background import BackgroundScheduler
from .settings import BASE_DIR
import os

import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


# The "apscheduler." prefix is hard coded
scheduler = BackgroundScheduler({
    # 'apscheduler.jobstores.default': {
    #     'type': 'sqlalchemy',
    #     'url': 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    # },
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '20'
    },
    'apscheduler.executors.processpool': {
        'type': 'processpool',
        'max_workers': '5'
    },
    'apscheduler.job_defaults.coalesce': 'false',
    'apscheduler.job_defaults.max_instances': '3',
    'apscheduler.timezone': 'UTC',
})


scheduler.start()
# scheduler.remove_all_jobs()
