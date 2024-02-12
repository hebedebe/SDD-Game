
class RoomData:
    def __init__(self, north, east, south, west, layout, entities):
        self.north = north
        self.east = east
        self.south = south
        self.west = west

        self.layout = layout
        self.entities = entities


rooms = {
    RoomData(1, 0, 0, 0, [], [])  # example level that contains nothing and has an entrance to the north
}