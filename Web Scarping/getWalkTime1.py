import requests

def get_walking_time(origin, destination, api_key):
    if(origin.isdigit()):
        origin = "Building "+ origin
    origin = origin + " Stanford, 94305"

    # Constructing the URL for the API request
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origin,
        "destinations": destination,
        "mode": "walking",
        "key": api_key
    }

    # Making the request to the Google Maps Distance Matrix API
    response = requests.get(base_url, params=params)

    # Checking if the request was successful
    if response.status_code == 200:
        # Parsing the response JSON
        result = response.json()

        # Checking if the 'duration' field is present
        elements = result["rows"][0]["elements"]
        if "duration" in elements[0]:
            walking_time = elements[0]["duration"]["text"]
            return walking_time
        else:
            # Handle cases where 'duration' is missing
            return "Duration not available"
    else:
        return "Error: API request unsuccessful."


# 读取源地址列表
source_addresses = []
with open("../User Interface (Main)/unique_locations_full_names.txt", "r") as file:
    source_addresses = file.read().splitlines()

# 定义目的地地址
destinations = ["Stanford Shopping Center, Stanford, CA, 94305",
                "Lake Lagunita, Stanford, CA, 94305",
                "CoHo, Stanford, CA, 94305",
                "McMurty Building, Stanford, CA, 94305",
                "Green Library, Stanford, CA, 94305"]

# 你的Google API密钥
api_key = "AIzaSyAg1UseWAyxs4GeoCR1nixTcnIs80cfVA4"

# 存储结果
results = []

# 对每个源地址计算到每个目的地的步行时间
for origin in source_addresses:
    walking_times = []
    for destination in destinations:
        walking_time = get_walking_time(origin, destination, api_key)
        walking_times.append(walking_time)
    results.append(walking_times)

# 将结果写入新的txt文件
with open("../Gathered Data/Walktime.txt", "w") as file:
    for result in results:
        file.write(",".join(result) + "\n")
