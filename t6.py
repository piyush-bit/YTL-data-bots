import json

# Specify the path to your JSON files
json_file_path1 = './c.json'
json_file_path2 = './a.json'

# Open the JSON files in read mode
with open(json_file_path1, 'r') as json_file1:
    data1 = json.load(json_file1)

with open(json_file_path2, 'r') as json_file2:
    data2 = json.load(json_file2)

# Extract the "data" array from the object in "a.json"
data2_array = data2.get("data", [])

# Create a dictionary to map "title" to the corresponding data in "a.json"
title_to_data = {item.get("title"): item for item in data2_array}

# Create a new list to store the combined data in the order of "c.json"
combined_data = []

# Iterate through the data in "c.json" and use the mapping dictionary to find corresponding data from "a.json"
for item_c in data1:
    subtopic_data = {
        "subtopic": item_c["subtopic"],
        "data": []
    }
    for item_data_c in item_c["data"]:
        title = item_data_c.get("title")
        if title in title_to_data:
            subtopic_data["data"].append(title_to_data[title])
    
    combined_data.append(subtopic_data)

# Create a new JSON file to store the combined data
json_file_path_combined = 'combined_data.json'

# Write the combined data to the new JSON file
with open(json_file_path_combined, 'w') as json_file_combined:
    json.dump(combined_data, json_file_combined, indent=4)

print(combined_data)
