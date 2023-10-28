
import json

# Specify the path to your JSON file
json_file_path1 = './c.json'
json_file_path2 = './a.json'


# Open the JSON file in read mode
with open(json_file_path1, 'r') as json_file1:
    # Parse the JSON data
    data1 = json.load(json_file1)

with open(json_file_path2, 'r') as json_file2:
    # Parse the JSON data
    data2 = json.load(json_file2)

data3 = data2["data"][0]["content"]
# Now, 'data' contains the contents of the JSON file as a Python dictionary or list
# You can access and manipulate the data as needed
c=0
data= []
for i in data1 :
    d = {
    "title": i["subtopic"],
    "content": []
    }

    for j in i["data"] :
        d["content"].append(data3[c])
        c+=1
    data.append(d)

data2["data"]=data
# Specify the file path where you want to save the JSON data
json_file_path = 'data.json'

# Open the file in write mode and write the JSON data to it
with open(json_file_path, 'w') as json_file:
    json.dump(data2, json_file, indent=4)  # Indent for pretty formatting (optional)


print(data)
