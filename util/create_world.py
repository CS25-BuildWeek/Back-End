from django.contrib.auth.models import User
from adventure.models import Room

Room.objects.all().delete()
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
        room_titles = ["Outside Cave Entrance", "Foyer"]
        room_descriptions = ["North of you, the cave mount beckons", """Dim light filters in from the south. Dusty
        passages run north and east."""]  
        while room_count < num_rooms:
            if direction > 0 and x < size_x - 4:
                room_direction = "e"
                x += 5
            elif direction < 0 and x > 0:
                room_direction = "w"
                x -= 5
            else:
                # If we hit a wall, turn north and reverse direction
                room_direction = "n"
                y += 2
                direction *= -1
            # Create a room in the given direction
            import random
            num = random.choice(range(0,8))
            room = Room(room_titles[num], room_descriptions[num], x, y)
            room.save()
            self.grid[y][x] = room
            if previous_room is not None:
                previous_room.connect_rooms(room, room_direction)
            # Update iteration variables
            previous_room = room
            room_count += 1
w = World()
num_rooms = 400
width = 20
height = 20
w.generate_rooms(width, height, num_rooms)
