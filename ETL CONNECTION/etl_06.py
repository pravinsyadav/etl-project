import os
import psycopg2
from dotenv import load_dotenv

# -----------------------------------
# 1. Load environment variables
# -----------------------------------

load_dotenv()


# -----------------------------------
# 2. Connect to PostgreSQL
# -----------------------------------

conn = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT"),
    database=os.getenv("PG_DATABASE"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD")
)

print("Connected to PostgreSQL")


# -----------------------------------
# 3. Create cursor
# -----------------------------------

cursor = conn.cursor()


# -----------------------------------
# 4. Execute source query
# -----------------------------------

cursor.execute("""
    SELECT id, mrnno
    FROM t_patient
    LIMIT 5
""")


# -----------------------------------
# 5. Get column names
# -----------------------------------

column_names = [
    description[0]
    for description in cursor.description
]


# -----------------------------------
# 6. Transformation function
# -----------------------------------

def transform_patient(record):

    try:

        transformed_record = {
            "patient_id": int(record["id"]),
            "patient_mrn": record["mrnno"].strip()
        }

        return transformed_record, None

    except (ValueError, AttributeError) as error:

        return None, str(error)


# -----------------------------------
# 7. Validation function
# -----------------------------------

def validate_patient(record):

    if record["id"] is None:
        return False, "id is null"

    if record["mrnno"] is None:
        return False, "mrnno is null"

    return True, None


# -----------------------------------
# 8. Output containers
# -----------------------------------

transformed_records = []
invalid_records = []


# -----------------------------------
# 9. Batch processing
# -----------------------------------

while True:

    rows = cursor.fetchmany(1000)

    if not rows:
        break

    print(f"Processing batch of {len(rows)} records")


    # -----------------------------------
    # 10. Process each row
    # -----------------------------------

    for row in rows:

        # Convert tuple → dictionary

        record = dict(zip(column_names, row))


        # -----------------------------------
        # 11. Validate
        # -----------------------------------

        is_valid, validation_error = validate_patient(record)

        if not is_valid:

            invalid_records.append({
                "record": record,
                "error": validation_error
            })

            continue


        # -----------------------------------
        # 12. Transform
        # -----------------------------------

        transformed_record, transformation_error = transform_patient(record)

        if transformation_error:

            invalid_records.append({
                "record": record,
                "error": transformation_error
            })

            continue


        # -----------------------------------
        # 13. Store successful record
        # -----------------------------------

        transformed_records.append(transformed_record)


# -----------------------------------
# 14. Print results
# -----------------------------------

print("\nTRANSFORMED RECORDS:")
print(transformed_records)

print("\nINVALID RECORDS:")
print(invalid_records)


# -----------------------------------
# 15. Close database resources
# -----------------------------------

cursor.close()
conn.close()

print("\nPostgreSQL connection closed")