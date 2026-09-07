import os 
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT"),
    database=os.getenv("PG_DATABASE"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
)

cursor = conn.cursor()
 
cursor.execute("select id,mrnno from t_patient order by id limit 5")

result = cursor.fetchall()

for row in result:
    print(row)

cursor.close()

conn.close()