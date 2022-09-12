from config import config
from db import DB
import psycopg2


def initiate_db():
    params = config()
    conn = psycopg2.connect(**params)
    return conn


