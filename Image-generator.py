from PIL import Image
import random
import json

# Each image is made up a series of traits
# The weightings for each trait drive the rarity and add up to 100%

background = ["Blue", "Orange", "Purple", "Red", "Yellow"]
background_weights = [30, 40, 15, 5, 10]

whale = ["Blue", "Brown", "Green", "Light_Blue"]
whale_weights = [25, 25, 25, 25]

eye = ["Blue", "Green", "Red", "Yellow"]
eye_weights = [25, 25, 25, 25]

cap = ["Red", "Yellow"]
cap_weights = [50,50]

# Dictionary variable for each trait.
# Each trait corresponds to its file name

background_files = {
    "Blue": "blue",
    "Orange": "orange",
    "Purple": "purple",
    "Red": "red",
    "Yellow": "yellow",
}

whale_files = {
    "Blue": "blue-whale",
    "Brown": "brown-whale",
    "Green": "green-whale",
    "Light_Blue": "lightblue-whale",
}

eye_files = {
    "Blue": "blue-eye",
    "Green": "green-eye",
    "Red": "red-eye",
    "Yellow": "yellow-eye"
}
cap_files = {
    "Red": "red-cap",
    "Yellow": "yellow-cap"
}
## Generate Traits

TOTAL_IMAGES = 30  # Number of random unique images we want to generate

all_images = []


# A recursive function to generate unique image combinations
def create_new_image():
    new_image = {}  #

    # For each trait category, select a random trait based on the weightings
    new_image["Background"] = random.choices(background, background_weights)[0]
    new_image["Whale"] = random.choices(whale, whale_weights)[0]
    new_image["Eye"] = random.choices(eye, eye_weights)[0]
    new_image["Cap"] = random.choices(cap, cap_weights)[0]

    if new_image in all_images:
        return create_new_image()
    else:
        return new_image


# Generate the unique combinations based on trait weightings
for i in range(TOTAL_IMAGES):
    new_trait_image = create_new_image()

    all_images.append(new_trait_image)
# Returns true if all images are unique
def all_images_unique(all_images):
    seen = list()
    return not any(i in seen or seen.append(i) for i in all_images)

print("Are all images unique?", all_images_unique(all_images))
# Add token Id to each image
i = 0
for item in all_images:
    item["tokenId"] = i
    i = i + 1
print(all_images)
# Get Trait Counts

background_count = {}
for item in background:
    background_count[item] = 0

whale_count = {}
for item in whale:
    whale_count[item] = 0

eye_count = {}
for item in eye:
    eye_count[item] = 0
cap_count = {}
for item in cap:
    cap_count[item] = 0

for image in all_images:
    background_count[image["Background"]] += 1
    whale_count[image["Whale"]] += 1
    eye_count[image["Eye"]] += 1
    cap_count[image["Cap"]] += 1


print(background_count)
print(whale_count)
print(eye_count)
#### Generate Metadata for all Traits
METADATA_FILE_NAME = './metadata/all-traits.json'
with open(METADATA_FILE_NAME, 'w') as outfile:
    json.dump(all_images, outfile, indent=4)
#### Generate Images
for item in all_images:

    im1 = Image.open(f'./trait-layers/backgrounds/{background_files[item["Background"]]}.jpg').convert('RGBA')
    im2 = Image.open(f'./trait-layers/whale/{whale_files[item["Whale"]]}.png').convert('RGBA')
    im3 = Image.open(f'./trait-layers/eyes/{eye_files[item["Eye"]]}.png').convert('RGBA')
    im4 = Image.open(f'./trait-layers/caps/{cap_files[item["Cap"]]}.png').convert('RGBA')
    im5 = Image.open(f'./trait-layers/skeleton/skeleton.png').convert('RGBA')




    #Create each composite
    com1 = Image.alpha_composite(im1, im2)
    com2 = Image.alpha_composite(com1, im3)
    com3 = Image.alpha_composite(com2, im4)
    com4 = Image.alpha_composite(com3, im5)

    #Convert to RGB
    rgb_im = com4.convert('RGB')
    file_name = str(item["tokenId"]) + ".png"
    rgb_im.save("./images/" + file_name)
#### Generate Metadata for each Image

f = open('./metadata/all-traits.json',)
data = json.load(f)


IMAGES_BASE_URI = "ADD_IMAGES_BASE_URI_HERE"
PROJECT_NAME = "ADD_PROJECT_NAME_HERE"

def getAttribute(key, value):
    return {
        "trait_type": key,
        "value": value
    }
for i in data:
    token_id = i['tokenId']
    token = {
        "image": IMAGES_BASE_URI + str(token_id) + '.png',
        "tokenId": token_id,
        "name": PROJECT_NAME + ' ' + str(token_id),
        "attributes": []
    }
    token["attributes"].append(getAttribute("Background", i["Background"]))
    token["attributes"].append(getAttribute("Whale", i["Whale"]))
    token["attributes"].append(getAttribute("Eye", i["Eye"]))
    token["attributes"].append(getAttribute("Cap", i["Cap"]))


    with open('./metadata/' + str(token_id), 'w') as outfile:
        json.dump(token, outfile, indent=4)
f.close()