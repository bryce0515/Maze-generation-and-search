# Maze-generation-and-search

Maze generation and search using DFS,BFS,Fringe,A*
================================
 NOTE: This code runs on Python2 
================================

===============================================================================

1- Maze Generation:
•	One command line
•	Change directory to Assign1
•	Run:		python Assign1.py nrRows nrCols maze.txt

Example:		python Assign1.py 10 10 maze.txt


2- To visualize the Maze, you can run the code as follows:

•	java GMaze maze.txt
===============================================================================

===============================================================================

3- Maze Search:
•	Run:		python method maze.txt rstart cstart rend cend path.txt

Methods supported: DFS, BFS, AStarZero, AStarEuclidean, AStarDynamic, and Fringe

Make sure rstart, and rend are less than the number of rows in maze,
and cstart, and cend are less than the number of columns in maze.

Example:		python Assign1.py BFS maze.txt 1 1 8 8 path.txt

The path will be created in path.txt


4- To visualize the Maze and path, you can run the code as follows:

•	java GMaze maze.txt path.txt

===============================================================================
