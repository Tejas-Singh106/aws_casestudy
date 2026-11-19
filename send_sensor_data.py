
import boto3
import csv
import json

REGION = "ap-south-1"
STREAM_NAME = "sensor-firehouse-stream"
CSV_FILE = "Activity10_Firehose_sensor_readings.csv"

firehose = boto3.client("firehose", region_name=REGION)

total = 0

with open(CSV_FILE, "r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    if not reader.fieldnames or "device_type" not in reader.fieldnames:
        raise ValueError("CSV must contain device_type column")

    for row in reader:
        response = firehose.put_record(
            DeliveryStreamName=STREAM_NAME,
            Record={
                "Data": (json.dumps(row) + "\n").encode("utf-8")
            }
        )

        total += 1
        print(f"Record {total} sent: {response['RecordId']}")

print(f"\nTotal records sent: {total}")
