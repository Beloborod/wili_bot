from mongoengine import connect
from configs.mongo_creds import config as mongo_creds


def connection():
    connect(mongo_creds['database'],
            host=mongo_creds['host'],
            port=mongo_creds['port'],
            username=mongo_creds['username'] if mongo_creds['use_authenticate'] else None,
            password=mongo_creds['password'] if mongo_creds['use_authenticate'] else None,
            authentication_source=mongo_creds['authentication_source'] if mongo_creds['use_authenticate'] else None
            )
