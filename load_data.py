
import boto3
import csv

dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-south-1'
)

def load_csv(table_name, filename):
    table = dynamodb.Table(table_name)

    with open(filename, 'r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)

        with table.batch_writer() as batch:
            for row in reader:

                # Store expiry_time as a Number
                if 'expiry_time' in row:
                    row['expiry_time'] = int(row['expiry_time'])

                batch.put_item(Item=row)

    print(f"Successfully loaded {filename} into {table_name}")

load_csv('sessions', 'Activity13_DynamoDB_sessions.csv')
load_csv('players', 'Activity13_DynamoDB_players.csv')

