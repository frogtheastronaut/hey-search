# join crawlres.json from each of the folders
import json

# List of folder names (bot_1 through bot_50)
FOLDER_NAMES = [
    "bot_1", "bot_2", "bot_3", "bot_4", "bot_5", "bot_6", "bot_7", "bot_8", "bot_9", "bot_10",
    "bot_11", "bot_12", "bot_13", "bot_14", "bot_15", "bot_16", "bot_17", "bot_18", "bot_19", "bot_20",
    "bot_21", "bot_22", "bot_23", "bot_24", "bot_25", "bot_26", "bot_27", "bot_28", "bot_29", "bot_30",
    "bot_31", "bot_32", "bot_33", "bot_34", "bot_35", "bot_36", "bot_37", "bot_38", "bot_39", "bot_40",
    "bot_41", "bot_42", "bot_43", "bot_44", "bot_45", "bot_46", "bot_47", "bot_48", "bot_49", "bot_50"
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
                print(f"wrote data from folder {folder}")
        except FileNotFoundError:
            print(f"folder '{folder}' does not exist/crawlres.json missing")
        except json.JSONDecodeError:
            print(f"file in folder '{folder}' has no valuable information")

    # combine data
    for data in combined_data:
        # each data format is a dictionary:
        # "url": "data"
        for item in data['site_known_data']:
            if item not in combined_data_processed:
                combined_data_processed.append({
                    "url": item,
                    "data": data['site_known_data'][item]
                })

    # put combined_data_processed into crawlres.json
    with open("crawlres.json", 'w') as file:
        json.dump(combined_data_processed, file, indent=4)
        print("crawlres.json HAS BEEN WRITTEN")
