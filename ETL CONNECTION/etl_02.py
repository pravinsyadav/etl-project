# connect to postgre sql and execute sql command 

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

# pg_host = os.getenv("PG_HOST")                # you can create like this and use that variable names in the psycopg2.connect 
# pg_port = os.getenv("PG_PORT")
# pg_database = os.getenv("PG_DATABASE")
# pg_user = os.getenv("PG_USER")
# pg_password = os.getenv("PG_PASSWORD")

pg_connection = psycopg2.connect(           # the varialbe name for psycopg2.connect will be same as given below 
    host=os.getenv("PG_HOST"),              # you can't change host to pg_host or any diff name 
    port=os.getenv("PG_PORT"),
    database=os.getenv("PG_DATABASE"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD")      
)

print("Connected to PostgreSQL")

cursor = pg_connection.cursor()   # cursor is the thing used to send SQL commands and receive results through that connection.        

cursor.execute("SELECT 1")       # it execute the sql and it doesn't mean python has already received the result 

result = cursor.fetchone()         # fetch one record and store it into result .. result came to python 

print(result)                    # print the result fetched from the database

cursor.close()                    # close the cursor 
pg_connection.close()            # close the connection 











    #           .env
    #            │
    #            ↓
    #     load_dotenv()
    #            │
    #            ↓
    #     os.getenv(...)
    #            │
    #            ↓
    #   PostgreSQL credentials
    #            │
    #            ↓
    #  psycopg2.connect(...)
    #            │
    #            ↓
    #    pg_connection
    #            │
    #            ↓
    #     cursor created
    #            │
    #            ↓
    #    cursor.execute()
    #            │
    #            ↓
    #   PostgreSQL executes SQL
    #            │
    #            ↓
    #    cursor.fetchone()
    #            │
    #            ↓
    #    Result comes to Python
    #            │
    #            ↓
    #       print(result)
    #            │
    #            ↓
    #     cursor.close()
    #            │
    #            ↓
    #    connection.close()