# Floor Plan Simulator

This project provides a Python-based data representation for a simple building floor plan, including rooms, floors, and the connections between them. It includes functionality to find paths between rooms and visualize the building layout.

## Files

- `models.py`: Contains the core data structures for the simulation:
    - `Room`: Represents a single room with properties like name, windows, lights, and doors connecting to adjacent rooms.
    - `Floor`: A collection of `Room` objects.
    - `Building`: The main class that holds the building structure (a collection of floors). It includes methods for finding paths and plotting the layout.
- `test_models.py`: Contains unit tests for the classes and methods in `models.py`. It uses the `unittest` framework to verify functionality and includes tests for pathfinding, modifying room properties, and plotting.

## Requirements

This project requires the following Python libraries:
- `matplotlib`
- `networkx`

## How to Run

### Running the Tests

To verify that all the components are working correctly, you can run the unit tests from the root directory of the project (`floor_plan`).

To run the tests with verbose output, which shows the result of each individual test case, use the following command:

```bash
python -m unittest -v test_models.py
```

### Viewing the Plots

The test file (`test_models.py`) is configured to generate and display plots for the building layout and for a found path. When you run the tests, `matplotlib` will open windows to show these visualizations. Simply close the plot windows to allow the test execution to complete.
