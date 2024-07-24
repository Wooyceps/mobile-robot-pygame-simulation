# Autonomous Mobile Robot (AMR) Simulation

## Description

This project is a simulation of an Autonomous Mobile Robot (AMR) using Pygame. The AMR can be controlled using keyboard inputs or by clicking on the screen to set a target position for the robot. The AMR plans its trajectory to reach the target position in the fastest possible combination of rotary and linear movement. The interface displays the current position (X, Y) and angle of the AMR.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Files](#files)
- [License](#license)
- [Contact](#contact)

## Installation

### Prerequisites

- Python
- pip

To install the project, follow these steps:

1. Clone the repository
2. Install the required packages using pip: `pip install -r requirements.txt`

## Usage

Run the `main.py` script to start the simulation.

## Files

- `AMR.py`: Contains the `AMR` class which represents the Autonomous Mobile Robot.
- `interface.py`: Contains the `Interface` class which represents the interface of the simulation.
- `assets.py`: Contains the assets used in the simulation such as color constants and screen dimensions.
- `a_star.py`: Contains the implementation of the A* pathfinding algorithm used by the AMR to plan its trajectory.
- `map.py`: Contains the `Map` class which represents the environment in which the AMR operates. It includes obstacles and the target position.
- `main.py`: Contains the main function which initializes and runs the simulation.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

[LinkedIn](https://www.linkedin.com/in/micha%C5%82-w%C3%B3jcik-562213266/)

[mwooycik@gmail.com](mailto:mwooycik@gmail.com)
