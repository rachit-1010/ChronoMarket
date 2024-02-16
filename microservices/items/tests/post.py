import requests
import json

# Replace with the correct URL for your API endpoint
url = "http://localhost:3901/api/item/add_item"

# Example data - modify this according to your application's requirements
data = {
    "user_id": "12345",
    "item_name": "Vintage Watch",
    "description": "A rare vintage watch from 1950",
    "watch_reference_number": "VN1950",
    "watch_model": "Vintage Classic",
    "watch_year": 1950,
    "brand": "VintageTime",
    "item_condition": "Good",
    "auction_won": 0,
    "starting_price": 5000,
    "bid_amount": 5200,
    "auction_start": "2023-01-01T00:00:00",
    "auction_deadline": "2023-01-15T00:00:00"
}

# Convert the data to JSON format
json_data = json.dumps(data)

# Set the content type to application/json
headers = {'Content-Type': 'application/json'}

# Send the POST request
response = requests.post(url, headers=headers, data=json_data)

# Print the response
print("Status Code:", response.status_code)
print("Response Body:", response.text)
