import requests
import os
GOOGLE_MAPS_API_KEY = os.environ["GOOGLE_MAPS_API_KEY"]
TOMTOM_API_KEY = os.environ["TOMTOM_API_KEY"]
# url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=52.5267256,13.4044622&radius=1500&type=restaurant&keyword=cruise&key={GOOGLE_MAPS_API_KEY}"
tomtom_url = f"https://api.tomtom.com/search/2/nearbySearch/.json?lat=52.5267&lon=13.404&radius=2000&categorySet=7315&view=Unified&relatedPois=all&key={TOMTOM_API_KEY}"
payload={}
headers = {}

response = requests.request("GET", tomtom_url, headers=headers, data=payload)

print(response.text)