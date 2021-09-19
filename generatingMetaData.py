import json
#### Generate Metadata for each Image

f = open('./metadata/all-traits.json',)
data = json.load(f)
IMAGES_BASE_URI = "ipfs://QmY3u4APPwLemcvCHwuvwgM33nkWrYZJqi49iNHry7zrhz"
PROJECT_NAME = "Weird Whale"

def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }
for i in data:
    token_id = i['tokenId']
    token = {
        "tokenId": token_id,
        "name": PROJECT_NAME + ' ' + str(token_id),
        "description": "Weird Creature that enjoys long swims in the ocean.",
        "image": IMAGES_BASE_URI +"/"+str(token_id) + '.png',
        "attributes": []
    }
    token["attributes"].append(getAttribute("Background", i["Background"]))
    token["attributes"].append(getAttribute("Whale", i["Whale"]))
    token["attributes"].append(getAttribute("Eye", i["Eye"]))
    token["attributes"].append(getAttribute("Cap", i["Cap"]))
    with open('./metadata/' + str(token_id), 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()