import os
import psycopg2
from dotenv import load_dotenv


# Load environment variables
load_dotenv()


# Connect to PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT"),
    database=os.getenv("PG_DATABASE"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD")
)

print("Connected to PostgreSQL")


# Create cursor
cursor = conn.cursor()


# Incremental ETL settings
last_processed_id = 100
batch_size = 5


# Validation function
def validate_patient(record):

    if record["patient_id"] is None:
        return False, "patient_id is null"

    if record["patient_email"] is None:
        return False, "patient_email is null"

    return True, None


# Start batch processing
while True:

    print(f"\nFetching records after ID: {last_processed_id}")


    # Extract + Transform in PostgreSQL
    cursor.execute("""
        SELECT
            id AS source_id,
            id AS patient_id,
            TRIM(email) AS patient_email
        FROM t_blooddonorregistration
        WHERE id > %s
        ORDER BY id
        LIMIT %s
    """, (last_processed_id, batch_size))


    # Fetch current batch
    rows = cursor.fetchall()


    # Stop when no records are left
    if not rows:
        print("No more records.")
        break


    print(f"Fetched {len(rows)} records")


    # Get column names
    column_names = [
        description[0]
        for description in cursor.description
    ]


    # Lists for valid and invalid records
    transformed_records = []
    invalid_records = []


    # Process each record
    for row in rows:

        # Convert tuple into dictionary
        record = dict(zip(column_names, row))


        # Validate record
        is_valid, validation_error = validate_patient(record)


        # If validation fails
        if not is_valid:

            invalid_records.append({
                "record": record,
                "error": validation_error
            })

            continue


        # SQL has already transformed the record
        transformed_records.append(record)


    # Print batch summary
    print("Valid records:", len(transformed_records))
    print("Invalid records:", len(invalid_records))


    # Display invalid records
    for invalid_record in invalid_records:

        print(
            "Invalid record:",
            invalid_record["record"],
            "| Error:",
            invalid_record["error"]
        )


    # Simulate ClickHouse loading
    print("Loading batch into ClickHouse...")


    # For now we assume loading succeeded
    load_success = True


    # Update watermark ONLY after successful load
    if load_success:

        last_processed_id = rows[-1][0]

        print("Batch loaded successfully.")
        print("New watermark:", last_processed_id)

    else:

        print("ClickHouse load failed.")
        print("Watermark not updated.")

        break


# Close cursor and connection
cursor.close()
conn.close()

print("\nETL completed.")