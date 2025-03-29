import json
from pathlib import Path
import Zipcode
import requests



from flask import Flask, request, jsonify




keys = str ('')

def get_lat_lng(zip_code, api_key):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={zip_code}&key={api_key}"
    response = requests.get(url)
    data = response.json()
#     for key in data['results']:{
#     print(key,":", data[key])
# }
    # print(data['results'][0])

    if data['status'] == 'OK':
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return lat, lng
    else:
        return None
# temp = get_lat_lng(78616, keys)
# print (temp)

#function that receives a list of zip codes
# list = ['78748','78660','78210']

def get_central_loc(zip_codes):
    # newList
    # print(newList);
    newList = []
    for zip in zip_codes:
        newList.append(get_lat_lng(zip, keys))
        # print(newList)
    
    lats = [point[0] for point in newList]
    longs = [point[1] for point in newList]
    
    avg_lat = sum(lats) / len(lats)
    avg_long = sum(longs) / len(longs)
    
    return (avg_lat, avg_long)
    
def get_park(lat, long, keys):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{long}&radius=5000&type=park&key={keys}"
    response = requests.get(url)
    data = response.json()
    #check for empty locations
    if data['status'] == 'OK':
        return data
#create new list Long_Lat_List of long/lat
#  for each zip code pass to get_lat_lng and add to
#  Long_Lat_List

#pass long Long_Lat_List to function to get "average" the central area to all the long lat

# lat_long_loc = get_central_loc(list)
# print("lat long loc")
# print(lat_long_loc)
# output = get_park(lat_long_loc[0], lat_long_loc[1], keys)
# print("Output:")
# print(output)
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'

@app.route('/data')
def greet2():
    return f'Hello, data!'


@app.route('/data', methods=['POST'])
def handle_post():
    data = request.get_json()
    # Process the data
    # output = get_central_loc(data["zip_codes"])
    central_loc = get_central_loc(data["zip_codes"])
    get_park(get_central_loc)
    response = {'message': 'Data received', 'data': data["zip_codes"]}
    return jsonify(response), 201
if __name__ == '__main__':
    app.run(debug=True)
