import os        # os is the python built in liabrary...we are using it to read environment variable
import psycopg2         # it is postgre driver .. it allows python to communicate with postgre sql 
from dotenv import load_dotenv     # its come from python-dotenv liabrary

load_dotenv()         # its job is to read .env file and load variables from .env file 


# we are storing connection details to variable conn we can give diff name to it... it just a object to store connection details
conn = psycopg2.connect(                     #psycopg2.connect means connect to postgre sql with following connection details 
    host=os.getenv("PG_HOST"),               # give me the value of the environment variable called PG_HOST
    port=os.getenv("PG_PORT"),               # give me the value of the environment variable called PG_PORT
    database=os.getenv("PG_DATABASE"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD")
)

print("Connected to PostgreSQL")

conn.close()





#                         PYTHON 
#                           ||
#                         CONNECTION
#                           ||
#                         POSTGRESQL
#                           ||
#                         CURSOR TO EXECUTE SQL
