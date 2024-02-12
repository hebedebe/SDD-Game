from glob import glob
from tqdm import tqdm


def load_rooms(path):
    rooms = []
    for file in tqdm(glob(path)):
        im = iio.imread(file)
        im.
        print(im.shape)
    return rooms


rooms = load_rooms("gamedata/rooms/*.png")
print(rooms)