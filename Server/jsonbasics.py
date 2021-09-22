import json

data = {
    "users":{
        "name": "William Williams",
        "age": 93
    }
}

with open("data_file.json", "w") as write_file:
    json.dump(data, write_file, indent=4)

json_str = json.dumps(data, indent=4)
print(json_str)
print(type(json_str))