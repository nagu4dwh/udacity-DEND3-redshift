import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries, create_table_queries, drop_table_queries

def drop_tables(cur, conn):
    """
    Drops all tables in a database
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()
    
def create_tables(cur, conn):
    """
    Creates all necessary tables in a database
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()
        
def load_staging_tables(cur, conn):
    """
    Load staging tables
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Insert data to specified tables
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()
        
def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()