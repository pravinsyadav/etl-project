import os
import psycopg2
from dotenv import load_dotenv


# -----------------------------------
# 1. Load environment variables
# -----------------------------------

load_dotenv()


# -----------------------------------
# 2. PostgreSQL connection
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
# 4. Starting watermark
# -----------------------------------

last_processed_id = 100

batch_size = 5


# -----------------------------------
# 5. Validation function
# -----------------------------------

def validate_patient(record):

    if record["id"] is None:
        return False, "id is null"

    if record["email"] is None:
        return False, "email is null"

    return True, None


# -----------------------------------
# 6. Transformation function
# -----------------------------------

def transform_patient(record):

    try:

        transformed_record = {
            "patient_id": int(record["id"]),
            "patient_email": record["email"].strip()
        }

        return transformed_record, None

    except(ValueError, AttributeError) as error:

        return None, str(error)


# -----------------------------------
# 7. Process batches
# -----------------------------------

while True:

    print(f"\nFetching records after ID: {last_processed_id}")


    # -----------------------------------
    # Extract
    # -----------------------------------

    cursor.execute("""
        SELECT id, email
        FROM t_blooddonorregistration
        WHERE id > %s
        ORDER BY id
        LIMIT %s
    """, (last_processed_id, batch_size))


    # -----------------------------------
    # Fetch current batch
    # -----------------------------------

    rows = cursor.fetchall()


    # -----------------------------------
    # Stop when no records remain
    # -----------------------------------

    if not rows:
        print("No more records.")
        break


    print(f"Fetched {len(rows)} records")


    # -----------------------------------
    # Get column names
    # -----------------------------------

    column_names = [
        description[0]
        for description in cursor.description
    ]


    transformed_records = []
    invalid_records = []


    # -----------------------------------
    # Process each row
    # -----------------------------------

    for row in rows:

        # Tuple → Dictionary

        record = dict(zip(column_names, row))


        # -----------------------------------
        # Validation
        # -----------------------------------

        is_valid, validation_error = validate_patient(record)


        if not is_valid:

            invalid_records.append({
                "record": record,
                "error": validation_error
            })

            continue


        # -----------------------------------
        # Transformation
        # -----------------------------------

        transformed_record, transformation_error = transform_patient(record)


        if transformation_error:

            invalid_records.append({
                "record": record,
                "error": transformation_error
            })

            continue


        transformed_records.append(transformed_record)


    # -----------------------------------
    # Show batch results
    # -----------------------------------

    print("Transformed records:", len(transformed_records))
    print("Invalid records:", len(invalid_records))


    # -----------------------------------
    # Simulate target loading
    # -----------------------------------

    print("Loading batch into ClickHouse...")


    # -----------------------------------
    # Update watermark
    # -----------------------------------

    last_processed_id = rows[-1][0]

    print("New watermark:", last_processed_id)


# -----------------------------------
# Close resources
# -----------------------------------

cursor.close()
conn.close()

print("\nETL completed.")