import logging          #logging is a built-in Python module used to record what is happening inside the ETL pipeline.


# This configures how logs should be written.
#asctime -> Date and time
#levelname -> INFO, WARNING, ERROR
#message - > actual log message 
logging.basicConfig(
    filename="etl_pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#this function is for the extraction phase
def extract_data():
    logging.info("Extraction started")

    # Database extraction logic
    data = [
        {"charge_id": 1, "patient_id": 101, "amount": 5000},
        {"charge_id": 2, "patient_id": None, "amount": 3000}
    ]

    logging.info("Extraction completed")
    return data


#this function performs data validation step 
def validate_data(data):
    valid_records = []
    rejected_records = []

    for record in data:
        if record["patient_id"] is None:
            rejected_records.append({
                "record": record,
                "error": "patient_id cannot be NULL"
            })

        elif record["amount"] <= 0:
            rejected_records.append({
                "record": record,
                "error": "amount must be greater than zero"
            })

        else:
            valid_records.append(record)
            
#return both lists.. this function will return two values 
    return valid_records, rejected_records


# this function represent the load step 
def load_data(valid_records):
    logging.info(
        "Loading %s valid records",
        len(valid_records)
    )

    # Insert valid records into target table


# this is the main controller function
def run_pipeline():
    try:
        logging.info("ETL pipeline started")

        data = extract_data()

        valid_records, rejected_records = validate_data(data)

        load_data(valid_records)

        logging.info(
            "Valid records: %s, Rejected records: %s",
            len(valid_records),
            len(rejected_records)
        )

        if rejected_records:
            logging.warning("Pipeline completed with rejected records")
            return "SUCCESS_WITH_REJECTS"

        logging.info("Pipeline completed successfully")
        return "SUCCESS"

    except Exception as error:
        logging.exception("Pipeline failed: %s", error)
        return "FAILED"

    finally:
        logging.info("ETL pipeline execution ended")


status = run_pipeline()
print(status)