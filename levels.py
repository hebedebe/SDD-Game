from glob import glob
from tqdm import tqdm
import PIL
from PIL import Image


def load_rooms(path):
    rooms = []
    for file in tqdm(glob(path)):
        img = Image.open(file)
        room_data = [[1 if img.getpixel((x, y)) == 19 else 0 for y in range(img.height)] for x in range(img.width)]
        rooms.append(room_data)

    return rooms


rooms = load_rooms("gamedata/rooms/*.png")
print(rooms)
