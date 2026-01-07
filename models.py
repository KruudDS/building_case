import matplotlib.pyplot as plt
import networkx as nx

class Room:
    def __init__(self, name, adjacent_rooms=None, windows=0, lights=0):
        self._name = name
        self._doors = {}
        self._adjacent_rooms = tuple(adjacent_rooms) if adjacent_rooms else ()
        self._windows = windows
        self._lights = lights

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def doors(self):
        return self._doors

    @property
    def adjacent_rooms(self):
        return self._adjacent_rooms

    @property
    def windows(self):
        return self._windows

    @windows.setter
    def windows(self, count):
        if count < 0:
            raise ValueError("Number of windows cannot be negative.")
        self._windows = count

    @property
    def lights(self):
        return self._lights

    @lights.setter
    def lights(self, count):
        if count < 0:
            raise ValueError("Number of lights cannot be negative.")
        self._lights = count

    def add_door(self, door_number, other_room):
        if other_room not in self.adjacent_rooms:
            raise ValueError(f"Cannot add a door to a non-adjacent room: {other_room.name}")
        if door_number in self._doors:
            raise ValueError(f"Door number {door_number} already exists in {self.name}")
        self._doors[door_number] = other_room

    def __repr__(self):
        return f"Room({self.name})"

class Floor:
    def __init__(self, rooms=None):
        self.rooms = rooms if rooms else []

    def add_room(self, room):
        self.rooms.append(room)

class Building:
    def __init__(self, floors=None):
        self.floors = floors if floors else []

    def add_floor(self, floor):
        self.floors.append(floor)

    def find_path(self, start_room, end_room):
        if not self.floors:
            return None

        # Assuming a single floor for this problem
        floor = self.floors[0]
        if start_room not in floor.rooms or end_room not in floor.rooms:
            return None

        #Create the BFS queue as FIFO
        queue = [[start_room]]

        # Keep track of visited rooms to avoid cycles
        visited = {start_room}

        #Run BFS
        while queue:
            #Get the first path from the queue
            path = queue.pop(0)
            current_room = path[-1]

            # Check if we reached the destination
            if current_room == end_room:
                return path

            for door_number, next_room in current_room.doors.items():
                if next_room not in visited:
                    visited.add(next_room)
                    new_path = list(path)
                    new_path.append(next_room)
                    queue.append(new_path)
        
        return None # No path found

    def add_door_between_rooms(self, room1, room2, door_num1, door_num2):
        if room2 not in room1.adjacent_rooms or room1 not in room2.adjacent_rooms:
            raise ValueError("Rooms are not adjacent.")
        
        room1.add_door(door_num1, room2)
        room2.add_door(door_num2, room1)

    def add_windows_to_room(self, room, count):
        room.windows += count

    def remove_windows_from_room(self, room, count):
        room.windows -= count

    def set_windows_in_room(self, room, count):
        room.windows = count

    def add_lights_to_room(self, room, count):
        room.lights += count

    def remove_lights_from_room(self, room, count):
        room.lights -= count

    def set_lights_in_room(self, room, count):
        room.lights = count

    def rename_room(self, room, new_name):
        room.name = new_name

    def plot_layout(self):
        if not self.floors:
            print("Cannot plot an empty building.")
            return

        # For simplicity, we'll plot the first floor
        floor = self.floors[0]
        
        G = nx.Graph()
        
        # Add rooms as nodes
        for room in floor.rooms:
            G.add_node(room.name)
            
        # Add doors as edges
        for room in floor.rooms:
            for other_room in room.doors.values():
                G.add_edge(room.name, other_room.name)

        # Create custom labels
        labels = {room.name: f"{room.name}\n Windows: {room.windows}, \n Doors: {len(room.doors)} \n Lights: {room.lights}" for room in floor.rooms}

        # Get positions for the nodes
        pos = nx.spring_layout(G, seed=42)  # Seed for reproducible layout
        
        plt.figure(figsize=(12, 8))
        
        # Draw the nodes (rooms) as rectangles
        nx.draw_networkx_nodes(G, pos, node_shape='s', node_size=5000, node_color='skyblue')
        
        # Draw the edges (doors)
        nx.draw_networkx_edges(G, pos, width=2.0, alpha=0.7, edge_color='gray')
        
        # Draw the labels (room names)
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_family='sans-serif')
        
        plt.title("Building Floor Plan")
        plt.axis('off') # Hide the axes
        plt.show()

    def plot_path(self, path):
        if not path:
            print("Cannot plot an empty path.")
            return

        floor = self.floors[0]
        G = nx.Graph()

        for room in floor.rooms:
            G.add_node(room.name)
        
        for room in floor.rooms:
            for other_room in room.doors.values():
                G.add_edge(room.name, other_room.name)

        pos = nx.spring_layout(G, seed=42)

        # Create labels with room details
        labels = {room.name: f"{room.name}\n Windows: {room.windows}, \n Doors: {len(room.doors)} \n Lights: {room.lights}" for room in floor.rooms}

        # Color nodes based on path
        path_room_names = [room.name for room in path]
        node_colors = ['lightgreen' if node in path_room_names else 'skyblue' for node in G.nodes()]

        # Identify edges in the path
        path_edges = list(zip(path_room_names, path_room_names[1:]))

        plt.figure(figsize=(12, 8))
        
        # Draw all nodes and edges
        nx.draw_networkx_nodes(G, pos, node_shape='s', node_size=5000, node_color=node_colors)
        nx.draw_networkx_edges(G, pos, width=2.0, alpha=0.7, edge_color='gray')

        # Highlight path edges
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=4.0, edge_color='green')
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_family='sans-serif')
        
        plt.title("Path between " + path_room_names[0] + " and " + path_room_names[-1])
        plt.axis('off')
        plt.show()
