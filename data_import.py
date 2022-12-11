import datetime
import random 
import requests


# List of users 
USERS = [
    {'id': '113', 'first_name': 'Sean', 'last_name': 'Coonce'},
    {'id': '224', 'first_name': 'Bill', 'last_name': 'Lawson'},
    {'id': '334', 'first_name': 'Shelby', 'last_name': 'Vaurier'},
    {'id': '441', 'first_name': 'Kian', 'last_name': 'Sarreshteh'},
    {'id': '541', 'first_name': 'Dave', 'last_name': 'Guttmann'},
    {'id': '667', 'first_name': 'Rob', 'last_name': 'Hoffmann'},
    {'id': '778', 'first_name': 'Zach', 'last_name': 'Truong'},
    {'id': '882', 'first_name': 'Ramsey', 'last_name': 'Villareal'},
    {'id': '996', 'first_name': 'Jake', 'last_name': 'Williamson'},
]

# List of financial institutions 
FIS = [
    {'id': 1000, 'name': 'Bank of Cleveland', 'type': 'Bank', 'state': 'OH'},
    {'id': 2000, 'name': 'Ohio Credit Union', 'type': 'Credit Union', 'state': 'OH'},
    {'id': 4000, 'name': 'State Bank of Texas', 'type': 'Bank', 'state': 'TX'},
    {'id': 5000, 'name': 'Keystone CU', 'type': 'Credit Union', 'state': 'TX'},
    {'id': 5000, 'name': 'Austin CU', 'type': 'Credit Union', 'state': 'TX'},
    {'id': 6000, 'name': 'Redwood City CU', 'type': 'Credit Union', 'state': 'CA'},
]

TRANASCTION_TYPES = ['buy', 'sell']
STATUSES = ['filled', 'pending', 'error']

# Insert 3000 random buy/sell transactions into elasticsearch
i = 0
while i < 3000:
    print(i)

    # Get a random user
    user = USERS[random.randint(0, len(USERS)-1)]

    # Get a financial institution
    fi = FIS[random.randint(0, len(FIS)-1)]

    # Get random USD value and converted BTC value
    usd_value = random.randint(50, 3000)
    price_btc = random.randint(16500, 18000)
    btc_value = usd_value / price_btc

    # Get random transaction_type 
    transaction_type = TRANASCTION_TYPES[
        random.randint(0, len(TRANASCTION_TYPES)-1)
    ]

    # Get a random status weighted towards 'filled'
    status = random.choices(STATUSES, weights=(60, 10, 20), k=1)[0]

    # Get a random date up to 60 days in the past
    date_created = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 100))
    date_last_updated = date_created + datetime.timedelta(minutes=random.randint(1, 20))

    # Create a random transaction object that will inserted into ES
    transaction_object = {
        "transaction_id": i,
        "dynamo_object_id": "DYDB-{}".format(i),
        "qldb_id": "QL-{}".format(i),
        "fi_id": "FI-{}".format(fi['id']),
        "fi_name": fi['name'],
        "fi_type": fi['type'],
        "fi_state": fi['state'],
        "account_id": "ACCT-{}".format(user['id']),
        "account_first_name": user['first_name'],
        "account_last_name": user['last_name'],
        "amount_fiat": usd_value,
        "amount_fiat_type": "USD",
        "amount_crypto": btc_value ,
        "amount_crypto_type": "BTC",
        "transaction_type": transaction_type,
        "price_btc": price_btc,
        "status": status,
        "date_created": date_created.isoformat(),
        "date_last_updated": date_last_updated.isoformat(),
    }
    pprint.pprint(transaction_object)

    # Add the document to elasticsearch 
    res = requests.api.post(
        'http://localhost:9200/transactions/_doc/',
        data=json.dumps(transaction_object),
        headers={'Content-type': 'application/json'},
    )
    print(res.status_code)
    i += 1
