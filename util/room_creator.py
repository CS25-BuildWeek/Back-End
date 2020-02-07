from django.contrib.auth.models import User
from adventure.models import Room

Room.objects.all().delete()


class World:
    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0

    def generate_rooms(self, size_x, size_y, num_rooms, Room):
        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        self.Room = Room
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x
        x = -5
        y = 0
        room_count = 0
        # Start generating rooms to the east
        direction = 1  # 1:east, -1:west
        # While there are rooms to be created...
        previous_room = None
        room_titles = ["Cave", "Church", "Outside CaveEnterance", "Foyer", "Narrow Passage", "Grand Overlook", "Treasure Chamber", "Maids Chamber", "King's Dining Room", "Courtyard", "Kitchen", "Guest Room",
                       "Grand Room", "Safe Room", "Guards Chamber", "Buttery", "Library", "Icehouse", "The Dungeion", "The Gatehouse", "Place of Arms", "The Gallery", "North Tower Room", "Stable House", "Barbican"]
        room_descriptions = ["North of you, the cave mount beckons", "Dim light filters in from the south. Dusty passages run north and east.", "You've found the long-lost treasure chamber! Sadly, it has already been completely emptied by earlier adventurers. The only exit is to the south.", "North of you, the cave mount beckons.", "Dim light filters in from the south. Dusty passages run north and east.", "A steep cliff appears before you, falling into the darkness. Ahead to the north, a light flickers in the distance, but there is no way across the chasm.", "The narrow passage bends here from west to north. The smell of gold permeates the air.", "Dark room full of old antiquities", "Large room with massive dinner table ", "Outdoor room with a large fountain and benches ", "Massive kitchen filled with pots, pans and various cookingware ", "Large room with a bed and sleeping quarters for any guests ", "Largest room in the Castle with the kings and queens throne inside ", "Small room filled with weapons to protect the Queen and King ",
                             "you've entered the guards chamber, it is filled with beds for the King's guard and swords ", "you've entered the buttery, it has a distinct smell of butter and other assorted foods ", "the dimly lit chamber filled with lanterns and books, a recipe for disaster! ", "you've entered the darkest room in the castle, filled with ice and extremely insulated to keep everything inside ;) ", "this is the most dangerous room in the house, most will not return once they enter... ", "you have entered the gatehouse, over looking the border walls of the castle ", "You have entered the most powerful room in the Castle, you can find weapons and armor in here! ", "the gallery is the most historical room in the castle, all prior kings and queens are remembered here! ", "this room over looks the edges of the Castle walls, great for protecting the Castle ", "you've entered the stable house, filled with beautiful horses and their not so beautiful stench!", "beware trespassers the sign says, this room is filled with traps! Tread carefully! "]
        while room_count < num_rooms:
            if direction > 0 and x < size_x - 1:
                room_direction = "e"
                x += 1
            elif direction < 0 and x > 0:
                room_direction = "w"
                x -= 1
            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n"
                y += 1
                direction *= -1
            # Create a room in the given direction
            import random
            num = random.choice(range(0, 25))
            room = Room(
                title=room_titles[num], description=room_descriptions[num], x=x, y=y)
            room.save()
            self.grid[y][x] = room
            if previous_room is not None:
                previous_room.connectRooms(room, room_direction)
            # Update iteration variables
            previous_room = room
            room_count += 1


w = World()
num_rooms = 225
width = 15
height = 15
Room = Room
w.generate_rooms(width, height, num_rooms, Room)
