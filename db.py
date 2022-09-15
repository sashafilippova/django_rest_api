import pandas as pd
import numpy as np
import math
from datetime import datetime as dt, timedelta as tdelta
import psycopg2.extras
from util import Eviction_Scraper, scrape_cases_by_id 

class DB: 
    def __init__(self, connection):
        self.conn = connection

    def execute_script(self, script_file):
        """
        Executes a given script.

        Inputs:
          script_file (str): path to the script file
        """
        with open(script_file, 'r') as script:
            c = self.conn.cursor()
            c.execute(script.read())
            c.close()
            # save changes in db
            self.conn.commit()

    
    def create_schema(self):
        """
        Creates tables listed in the create.sql file 
        """
        self.execute_script('create.sql')


    def inject_data(self, pd_df, table_name):
        """
        Injects data into a table in db. Before adding records from data_path, 
          the method removes duplicate records and replaces NaN values with None.

        Inputs:
          pd_df (pandas DataFrame): data
          table_name (str): name of the table in db
        """

        assert len(pd_df) > 0, 'No records were found to add to the database'

        pd_df = pd_df.drop_duplicates()
        pd_df = pd_df.replace({np.nan: None})  
        columns = f"{tuple(pd_df.columns)}".replace("'", "") 

        # convert pandas df into a list of tuples
        records_lst = list(pd_df.to_records(index=False))

        query = f"""INSERT INTO {table_name} {columns} VALUES %s;"""

        with self.conn.cursor() as c:
            psycopg2.extras.execute_values(cur = c, sql = query, argslist = records_lst)
            self.conn.commit()


    def query_all_records(self, table_name):
        """
        Returns all records from the table_name in db.

        Inputs:
          table_name (str): name of the table in db
        
        Returns a list (lst) of json objects.
        """
        query = f"""SELECT * FROM {table_name};"""

        with self.conn.cursor() as c:
            c.execute(query)
            data = c.fetchall() # list with tuples where each tuple is an observation
            col_names = [col_name[0] for col_name in c.description]
        
        return convert_result_to_json(data, col_names)
    

    def add_new_records(self, end_date = None):
        """
        Scrapes new eviction records from the court website and inputs them into db.
        The period for scraping is from the most recent filind date in db and until 
        present date if end_date is None. Otherwise, records will be scraped until 
        the provided end_date.

        Inputs:
          end_date (str) format mmddyyyy
        """
        with self.conn.cursor() as c:
            # get the most recent filed_date from db
            c.execute('select max(filed_date) from eviction_records;')
            last_filed_date = c.fetchall()[0][0]    #datetime.date data format

        start_date = last_filed_date + tdelta(days = 1)
        start_date = start_date.strftime("%m%d%Y")

        if end_date is None:
            if (start_date + tdelta(days = 90)) >= dt.today().date():
                end_date = dt.today().date()
            else:
                end_date = start_date + tdelta(days = 90)
            end_date = end_date.strftime("%m%d%Y")
        
        pd_df = Eviction_Scraper(start_date, end_date).run_scraper()
        self.inject_data(pd_df, 'eviction_records')

    
    def update_existing_records_disposition(self, records_per_batch = 500):
        """
        Identifies records in db with missing disposition and scrapes them 
          to update in db.
        """
        with self.conn.cursor() as c:
            c.execute('select case_id from eviction_records where disposition is NULL;')
            records_with_missing_disposition = [record[0] for record in c.fetchall()] 
        
        record_batches = list()
        for i in range(0, len(records_with_missing_disposition), records_per_batch):
            record_batches.append(records_with_missing_disposition[i:i + records_per_batch])
        
        for batch in record_batches:
            scraped_eviction_cases, _ = scrape_cases_by_id(batch)
            df = pd.DataFrame(scraped_eviction_cases)
            df = df.filter(['case_id', 'disposition', 'disposition_date', 'last_updated'])
            columns = f"{tuple(df.columns)}".replace("'", "")

            # convert pandas df into a list of tuples
            records_lst = list(df.to_records(index=False))

            query = f"""UPDATE eviction_records AS e SET
                            disposition = c.disposition
                            disposition_date = c.disposition_date
                            last_updated = c.last_updated
                        FROM (VALUES  %s 
                        ) AS c {columns}
                        WHERE c.case_id = e.case_id;"""

            with self.conn.cursor() as c:
                psycopg2.extras.execute_values(cur = c, sql = query, argslist = records_lst)
                self.conn.commit()



####### UTILITY FUNCTIONS ###########

def convert_result_to_json(data, headers):
    """
    Converts input data into a list of json objects where each 
    object is an observation/row.

    Inputs:
      data (lst): a list of tuples where each tuple is a data row.
      headers (lst): a list of column names.

    Returns (lst) 
    """
    result = [dict(zip(headers, row)) for row in data]
    return result
        


