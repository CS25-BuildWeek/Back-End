from adventure.models import Player, Room
import random

Room.objects.all().delete()

rooms = {
    1: {"title": "Cave",
        "description": "dark spooky cave"},
    2: {"title": "Church",
        "description": "grand cathedral"},
    3: {"title": "Outside Cave Entrance",
        "description": "North of you, the cave mount beckons."},
    4: {"title": "Foyer",
        "description": "Dim light filters in from the south. Dusty passages run north and east."},
    5: {"title": "Grand Overlook",
        "description": "A steep cliff appears before you, falling into the darkness. Ahead to the north, a light flickers in the distance, but there is no way across the chasm."},
    6: {"title": "Narrow Passage",
        "description": "The narrow passage bends here from west to north. The smell of gold permeates the air."},
    7: {"title": "Treasure Chamber",
        "description": "You've found the long-lost treasure chamber! Sadly, it has already been completely emptied by earlier adventurers. The only exit is to the south."},
    8: {"title": "Maids Chamber",
        "description": "Dark room full of old antiquities"},
    9: {"title": "King's Dining Room",
        "description": "Large room with massive dinner table "},
    10: {"title": "Courtyard",
        "description": "Outdoor room with a large fountain and benches "},
    11: {"title": "Kitchen",
        "description": "Massive kitchen filled with pots, pans and various cookingware "},
    12: {"title": "Guest Room",
        "description": "Large room with a bed and sleeping quarters for any guests "},
    13: {"title": "Grand Room",
        "description": "Largest room in the Castle with the kings and queens throne inside "},
    14: {"title": "Safe Room",
        "description": "Small room filled with weapons to protect the Queen and King "},
    15: {"title": "Guards Chamber",
        "description": "you've entered the guards chamber, it is filled with beds for the King's guard and swords "},
    16: {"title": "Buttery",
        "description": "you've entered the buttery, it has a distinct smell of butter and other assorted foods "},
    17: {"title": "Library",
        "description": "the dimly lit chamber filled with lanterns and books, a recipe for disaster! "},
    18: {"title": "Icehouse",
        "description": "you've entered the darkest room in the castle, filled with ice and extremely insulated to keep everything inside ;) "},
    19: {"title": "The Dungeon",
        "description": "this is the most dangerous room in the house, most will not return once they enter... "},
    20: {"title": "The Gatehouse",
        "description": "you have entered the gatehouse, over looking the border walls of the castle "},
    21: {"title": "Place of Arms",
        "description": "You have entered the most powerful room in the Castle, you can find weapons and armor in here! "},
    22: {"title": "The Gallery",
        "description": "the gallery is the most historical room in the castle, all prior kings and queens are remembered here! "},
    23: {"title": "North Tower Room",
        "description": "this room over looks the edges of the Castle walls, great for protecting the Castle "},
    24: {"title": "Stable House",
        "description": "you've entered the stable house, filled with beautiful horses and their not so beautiful stench!"},
    25: {"title": "Barbican",
        "description": "beware trespassers the sign says, this room is filled with traps! Tread carefully! "},

} 
class Room:
    
    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name
        self.description = description
        self.n_to = None
        self.s_to = None
        self.e_to = None
        self.w_to = None
        self.x = x
        self.y = y

    def __repr__(self):
        if self.e_to is not None:
            return f"({self.x}, {self.y}) -> ({self.e_to.x}, {self.e_to.y})"
        return f"({self.x}, {self.y})"
        
    def connect_rooms(self, connecting_room, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        reverse_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}
        reverse_dir = reverse_dirs[direction]
        setattr(self, f"{direction}_to", connecting_room)
        setattr(connecting_room, f"{reverse_dir}_to", self)
        
    def get_room_in_direction(self, direction):
        '''
        Connect two rooms in the given n/s/e/w direction
        '''
        return getattr(self, f"{direction}_to")


class World:

    def __init__(self):
        self.grid = None
        self.width = 0
        self.height = 0
    def generate_rooms(self, size_x, size_y, num_rooms):
        
        # Initialize the grid
        self.grid = [None] * size_y
        self.width = size_x
        self.height = size_y
        for i in range(len(self.grid)):
            self.grid[i] = [None] * size_x
        x = -5
        y = 0
        room_count = 0
        # Start generating rooms to the east
        direction = 1 #1:east, -1:west
        # While there are rooms to be created...
        previous_room = None
        room_titles = rooms['name']
        room_descriptions = rooms['description']
        # room.save()
        while room_count < num_rooms:
            if direction > 0 and x < size_x - 5:
                room_direction = "e"
                x += 5
            elif direction < 0 and x > 0:
                room_direction = "w"
                x -= 5
            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n"
                y += 5
                direction *= -1
            # Create a room in the given direction
            import random
            num = random.choice(range(0,5))
            room = Room(room_count, room_titles[num], room_descriptions[num], x, y)
            room.save()
            self.grid[y][x] = room
            if previous_room is not None:
                previous_room.connect_rooms(room, room_direction)
            # Update iteration variables
            previous_room = room
            room_count += 1
    def print_rooms(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''

        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"

        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid) # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"

        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"

        # Print string
        print(str)


w = World()
num_rooms = 400
width = 20
height = 20
w.generate_rooms(width, height, num_rooms)
w.print_rooms()

players=Player.objects.all()
for p in players:
    p.currentRoom=w.grid[0][0].id
    p.save()
