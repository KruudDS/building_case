import unittest
from models import Room, Floor, Building

class TestBuilding(unittest.TestCase):

    def setUp(self):
        # Create rooms
        self.room1 = Room("Office Room 1", windows=2, lights=3)
        self.room2 = Room("Kitchen", windows=1, lights=2)
        self.room3 = Room("Office Room 2", windows=1, lights=1)
        self.room4 = Room("Bathroom", windows=0, lights=1)
        self.room5 = Room("Corridor", windows=0, lights=4)
        self.room6 = Room("Office Room 3", windows=1, lights=2)
        self.room7 = Room("Office Room 4", windows=0, lights=0)

        # Define adjacency
        self.room1._adjacent_rooms = (self.room5,)
        self.room2._adjacent_rooms = (self.room5,)
        self.room3._adjacent_rooms = (self.room5,)
        self.room4._adjacent_rooms = (self.room5, self.room6)
        self.room5._adjacent_rooms = (self.room1, self.room2, self.room3, self.room4, self.room6)
        self.room6._adjacent_rooms = (self.room5, self.room7)
        self.room7._adjacent_rooms = (self.room6,)

        # Create a floor and add rooms
        self.floor = Floor(rooms=[self.room1, self.room2, self.room3, self.room4, self.room5, self.room6, self.room7])

        # Create a building and add the floor
        self.building = Building(floors=[self.floor])

        # Add doors
        self.building.add_door_between_rooms(self.room1, self.room5, 1, 1)
        self.building.add_door_between_rooms(self.room2, self.room5, 1, 2)
        self.building.add_door_between_rooms(self.room3, self.room5, 1, 3)
        self.building.add_door_between_rooms(self.room4, self.room5, 1, 4)
        self.building.add_door_between_rooms(self.room6, self.room5, 1, 5)
        self.building.add_door_between_rooms(self.room6, self.room7, 2, 1)

    def test_find_path(self):
        path = self.building.find_path(self.room1, self.room7)
        self.assertIsNotNone(path)
        self.assertEqual(path, [self.room1, self.room5, self.room6, self.room7])

        self.building.plot_path(path)

        path_same_room = self.building.find_path(self.room1, self.room1)
        self.assertEqual(path_same_room, [self.room1])

        # Create a disconnected room
        room8 = Room("Isolated Room")
        self.floor.add_room(room8)
        path_no_connection = self.building.find_path(self.room1, room8)
        self.assertIsNone(path_no_connection)

    def test_add_door(self):
        # Test adding a valid door
        room8 = Room("New Room", adjacent_rooms=[self.room1])
        self.room1._adjacent_rooms += (room8,)
        self.floor.add_room(room8)
        self.building.add_door_between_rooms(self.room1, room8, 2, 1)
        self.assertIn(2, self.room1.doors)
        self.assertEqual(self.room1.doors[2], room8)
        self.assertIn(1, room8.doors)
        self.assertEqual(room8.doors[1], self.room1)

        # Test adding a door to a non-adjacent room
        with self.assertRaises(ValueError):
            self.building.add_door_between_rooms(self.room1, self.room2, 3, 2)

    def test_modify_windows(self):
        self.building.add_windows_to_room(self.room1, 2)
        self.assertEqual(self.room1.windows, 4)
        self.building.remove_windows_from_room(self.room1, 1)
        self.assertEqual(self.room1.windows, 3)
        self.building.set_windows_in_room(self.room1, 5)
        self.assertEqual(self.room1.windows, 5)
        with self.assertRaises(ValueError):
            self.room1.windows = -1

    def test_modify_lights(self):
        self.building.add_lights_to_room(self.room2, 1)
        self.assertEqual(self.room2.lights, 3)
        self.building.remove_lights_from_room(self.room2, 2)
        self.assertEqual(self.room2.lights, 1)
        self.building.set_lights_in_room(self.room2, 4)
        self.assertEqual(self.room2.lights, 4)
        with self.assertRaises(ValueError):
            self.room2.lights = -1

    def test_rename_room(self):
        self.building.rename_room(self.room3, "Copy machine Room")
        self.assertEqual(self.room3.name, "Copy machine Room")

    def test_plot(self):
        self.building.plot_layout()

if __name__ == '__main__':
    unittest.main()
