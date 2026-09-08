

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host = os.getenv("PG_HOST"),
    port = os.getenv("PG_PORT"),
    database = os.getenv("PG_DATABASE"),
    user = os.getenv("PG_USER"),
    password = os.getenv("PG_PASSWORD")
)


cursor = conn.cursor()

cursor.execute("""
               select id, mrnno from t_patient limit 5
               """)

result = cursor.fetchall()  
        
column_names = [description[0] for description in cursor.description]


# here we are preparing a container which will store our python dictionaries
records = []


#it will convert tuple to dictionary
for row in result:
    record = dict(zip(column_names,row))
    records.append(record) 
print(records)



# this is a function .. it is accepting one argument record .... (record = 'id':101, 'mrnno':ILBS.0000095') 
# Take one patient record, try to transform it, and if transformation succeeds, return the transformed record with no error. 
# If a known transformation error occurs, return no record and the error message instead of crashing the pipeline.
def transform_patient(record):
    try:
        # we are creating a new dictionary transformed_record
        transformed_record = {
            'patient_id': int(record['id']),
            'patient_mrn': record['mrnno'].strip()
        }
        # here we are sending two values we want to see wethere 1. What is the transformed record? 2. Did an error occur?
        return transformed_record, None
    
    # If a ValueError OR AttributeError happens inside the try block, catch that error and store it in the variable error.
    except (ValueError, AttributeError) as error:
        return None, str(error)
    
    
    
# This function receives one patient record.
# Its job is NOT to transform the record.
# Is this record acceptable for further processing?
def validate_patient(record):
    if record['id'] is None:
        return False, 'id is null'
    if record['mrnno'] is None:
        return False, 'mrnno is null'
    return True, None


# created two empty lists
transformed_records = []
invalid_records = []


#process every patient 
for record in records:
    #this is where the function gets called for validation 
    is_valid, validation_error = validate_patient(record)
    if not is_valid:
        invalid_records.append({
            "record": record,
            "error": validation_error
        })
        continue
    transformed_record, transformation_error = transform_patient(record)
    if transformation_error:
        invalid_records.append({
            "record": record,
            "error": transformation_error
        })
        continue
    transformed_records.append(transformed_record)

print(transformed_records)
print(invalid_records)

cursor.close()
conn.close()