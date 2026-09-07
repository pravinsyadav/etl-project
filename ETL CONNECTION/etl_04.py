import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

pg_connection = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT"),
    database=os.getenv("PG_DATABASE"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD")
)

print("Connected to PostgreSQL")

cursor = pg_connection.cursor()

cursor.execute("""
    SELECT id, mrnno
    FROM t_patient
    LIMIT 5
""")

# After executing the query, the cursor knows information about the returned columns.
# cursor.description contains metadata about those columns.
# [description[0]] is the column name 
column_names = [description[0] for description in cursor.description]

print("Columns:", column_names)

rows = cursor.fetchall()


# zip() is used to pair them 
# dict() conver data into dictionary
for row in rows:
    record = dict(zip(column_names, row))
    print(record)

cursor.close()
pg_connection.close()