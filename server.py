from config import config
from db import DB
from util import Eviction_Scraper
import psycopg2


def initiate_db():
    params = config()
    conn = psycopg2.connect(**params)
    return conn

# will be opening and closing db connection from the server
#conn.close()



