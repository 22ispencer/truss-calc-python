# Simple Truss Calculator

This is a project designed to solve the internal forces of statically determinate trusses.

## How to use

Commands

- new
  - node - adds a new node (joint)
    - x - the x coordinate of the node
    - y - the y coordinate of the node
    - x_support - whether or not the node has support in the x axis
    - y_support - whether or not the node has support in the y axis
    - ext_force - an array containing the x force and y force ([x_force, y_force])
  - member - adds a new member between nodes
    - node_1 - the first node of the member
    - node_2 - the second node of a member
  - force - updates the force on a specific joint
- solve
- save - saves the current configuration to a json file
- load - loads a json file with the specified for
