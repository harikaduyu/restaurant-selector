import requests
import json


def update_restaurant_list():
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json][timeout:25];
    // gather results
    (
    // query part for: “amenity=restaurant”
    node["amenity"="restaurant"](52.52,13.40, 52.53,13.42);
    );
    // print results
    out body;
    >;
    out skel qt;
    """
    response = requests.get(overpass_url, 
                            params={'data': overpass_query})
    data = response.json()
    elements = data["elements"]
    restaurants = []
    for element in elements:
        restaurant = element["tags"]
        restaurant["lat"] = element["lat"]
        restaurant["lon"] = element["lon"]
        restaurant["id"] = element["id"]
        restaurants.append(restaurant)
    
    json_object = json.dumps(restaurants, indent=4)
    with open("restaurant_list.json", "w") as outfile:
        outfile.write(json_object)

if __name__ == '__main__':

    update_restaurant_list()
