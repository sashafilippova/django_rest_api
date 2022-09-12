import pandas as pd
import numpy as np
import psycopg2.extras

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


    def inject_data(self, data_path, table_name):
        """
        Injects data into a table in db.

        Inputs:
          data_path (str) path to CSV file containing data
          table_name (str) name of the table in db
        """

        pd_df = pd.read_csv(data_path)
        columns = f"{tuple(pd_df.columns)}".replace("'", "")  

        # drop duplicates, drop records with missing D or P names. Replace NaN values
        pd_df = pd_df.drop_duplicates()
        pd_df = pd_df.replace({np.nan: None})  

        # convert pandas df into a list of tuples
        records_lst = list(pd_df.to_records(index=False))


        query = f"""INSERT INTO {table_name} {columns} VALUES %s;"""

        with self.conn.cursor() as c:

            psycopg2.extras.execute_values(cur = c, sql = query, argslist = records_lst)
            self.conn.commit()
        
        print('is cursor closed: ', c.closed)


