# join crawlres.json from each of the folders
import json

# List of folder names
FOLDER_NAMES = [
    "alfa",
    "bravo",
    "charlie",
    "delta",
    "echo",
    "foxtrot",
    "golf",
    "hotel",
    "india",
    "juliet",  
    "kilo",
    "lima",
    "mike",
    "november",
    "oscar",
    "papa",
    "quebec",
    "romeo",
    "sierra",
    "tango",
    "uniform",
    "victor",
    "whiskey",
    "xray",
    "yankee",
    "zulu"
]

combined_data = []
combined_data_processed = []
if __name__ == "__main__":
    # Get crawlres.json content from each folder
    for folder in FOLDER_NAMES:
        try:
            with open(f"{folder}/crawlres.json", 'r') as file:
                data = json.load(file)
                combined_data.append(data)
        except FileNotFoundError:
            print(f"Folder '{folder}' does not exist/crawlres.json missing")
        except json.JSONDecodeError:
            print(f"File in folder '{folder}' has no valuable information")

    # combine data
    for data in combined_data:
        # Site known data URL -> site_known_data[0]
        # Site known data DATA -> site_known_data[1]

        # If URL not in combined_data_processed['url']
        if data['site_known_data'] not in combined_data_processed:
            for item in data['site_known_data']:
                if item not in combined_data_processed:
                    combined_data_processed.append(item)

    # put combined_data_processed into crawlres.json
    with open("crawlres.json", 'w') as file:
        json.dump(combined_data_processed, file, indent=4)
        print("crawlres.json HAS BEEN WRITTEN")
