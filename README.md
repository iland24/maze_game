# Zen Maze
Implemented using: python 3.11.5, pygame 2.5.1

<p align="center">
  <img src="https://github.com/iland24/maze_game/blob/main/assets/example_maze.PNG" alt="Sublime's custom image" width="300"/>
</p>

This is an exit finding maze game. Mouse and keyboard are needed to play this game.
Under the pygame framework, maze generating algorithm is used to generate new maze every time player clicks on a level (easy, medium, hard).
There is only one correct path from start to finish.

## Maze Generation
Grid frame of the maze is a nested list. Node object was added to the grid and contains directions (or neighbors) which it can go to.
Direction to parents and the selected directions each node takes makes the path of the maze. 
Start and end node is separated when the maze initializes to be in a diagonal position. 

After implementing the maze generating algorithm, I learned that I was using the "Hunt and Kill" maze generating algorithm. 
In the hunt mode, the algorithm branches out until it meets a dead end or the end node. 
Once it reaches a deadend, it goes into the kill mode, finding new path from visited nodes.
If there are no more paths that can be branched out from visited nodes, the algorithm finishes.

More of different types of  maze generating algorithms are explained here:
https://www.jamisbuck.org/presentations/rubyconf2011/index.html#title-page

The algorithm was tuned so that it sticks either to the wall or visited nodes when finding paths to make nice looking mazes.

## Pygame Framework
To make the maze in pygame, rectangles were generated for the walls, player and the end location. 
The game was designed so that when the player rectangle collides with the wall it stops moving. 
So, the player can only move along the path of the maze.

Button.py was feched from the following repository:
https://github.com/baraltech/Menu-System-PyGame

Background music and the song that comes out when maze is finished are both from bensound, a copyright free music website.

\
Thanks for reading and enjoy the game! 
