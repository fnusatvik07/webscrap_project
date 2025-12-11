import requests
from pprint import pprint
from dotenv import load_dotenv 
load_dotenv()
import os 

username=os.getenv("OXYLABS_USERNAME")
password=os.getenv("OXYLABS_PASSWORD")
# Structure payload.
payload = {
    'source': 'amazon_product',
    'query': 'B0FJ2H6LK4',
    'geo_location': '90210',
    'parse': True
}

# Get response.
response = requests.request(
    'POST',
    'https://realtime.oxylabs.io/v1/queries',
    auth=(username,password),
    json=payload,
)

# Print prettified response to stdout.
print(response.json())