import copy  # Used in expand function
import sys
import time # To calculate time taken
import math

def main():
    # This is the main function which takes input from user and calls different functions according to user's choice
    print("8-puzzle solver\n")
    # Note: The goal state here is hardcoded. The assumption is the goal state remains the same.
    goal_state = ([1, 2, 3], [4, 5, 6], [7, 8, 0])
    puzzleoption = int(
        input("Enter 1 to run the default pre-loaded puzzle.\nEnter 2 to enter your own puzzle\n"))
    if puzzleoption == 1:
        # execute default puzzle
        print("Initial state of default puzzle is:\n")
        print(
            "-------------\n| 1 | 2 | 3 |\n-------------\n| 4 | 0 | 6 |\n-------------\n| 7 | 5 | 8 |\n-------------\n")
        print("Goal state of default puzzle is:\n")
        print(
            "-------------\n| 1 | 2 | 3 |\n-------------\n| 4 | 5 | 6 |\n-------------\n| 7 | 8 | 0 |\n-------------\n")
        #hard-coded initial state
        initial_state = ([1, 2, 3], [4, 0, 6], [7, 5, 8])


    elif puzzleoption == 2:
        print("Provide the initial state to solve this problem.Represent blank space with zero. \n")
        # Reading first row
        irow1 = input('First row, use spaces as delimiters between numbers: ')
        # Reading second row
        irow2 = input('Second row, use spaces as delimiters between numbers: ')
        # Reading the third row
        irow3 = input('Third row, use spaces as delimiters between numbers: ')

        print('\n')

        # Combining input into a puzzle
        # This will be list of lists
        irow1 = [int(float(x)) for x in irow1.split(' ')]
        irow2 = [int(float(x)) for x in irow2.split(' ')]
        irow3 = [int(float(x)) for x in irow3.split(' ')]

        initial_state = irow1, irow2, irow3
        print("Initial state of the puzzle is:\n")
        print(initial_state)
        print("The goal state of the puzzle is:\n")
        print(goal_state)
    # handling the invalid case
    else:
        print("Invalid!!. Enter 1/2\n")
        return -1

    # Make a choice of algorithm you want to use
    print("Choose the search algorithm to solve this problem\n")
    algooption = int(input(
        "1. Uniform cost search \n2. A* with the Misplaced Tile heuristic\n3. A* with the Manhattan Distance heuristic\n"))
    # Calling the general search function
    generalsearch(algooption, initial_state, goal_state)


# create node data structure to create/print nodes
class node:
    def __init__(self, state):
        self.state = state # stores the list of lists i.e actual value of the nodes Eg: [[1,2,3][4,0,6][0,7,8]]
        self.depth = 0  # g(n)
        self.heuristic = 0  # h(n)


def generalsearch(algooption, initial_state, goal_state):
    # To calcuate time taken to reach goal state
    initialTime = time.time()
    # queue to store all the expannded nodes
    queue = []
    # hashMap to save all the visited node and avoid visting repeated states
    hashMap = []
    # Count to keep track of nodes expanded
    number_of_nodes_expanded = 0

    # Passing the user input / default input to create the node data structure
    current_node = node(initial_state)
    # Initializing value of depth to 0 to indicate it starts from root and keep track of depth of the solution
    current_node.depth = 0
    # Add the node to queue and store it is visited list
    queue.append(current_node)
    hashMap.append(current_node.state)
    while True:
        # sort the queue to based on g(n)+h(n) with lowest cost node in the first to pop
        queue = sorted(queue, key=lambda n: (n.depth + n.heuristic, n.depth))
        # if there are no nodes in queue left and goal state is not reached
        if len(queue) == 0:
            print("Search exhausted\n")
            sys.exit(0)
        # On pop check if the node is goal state, if yes , print depth, nodes expanded and time taken
        parent_node = queue.pop(0)
        if parent_node.state == goal_state:
            print("Goal state reached")
            print(parent_node.state)
            print("Solution found at depth/cost of ", parent_node.depth)
            print("Number of expanded nodes:", number_of_nodes_expanded)
            endTime = time.time()
            print("Time taken :", round((endTime - initialTime),4), "seconds")
            return
        # Else expand all the children of popped node
        expanded_nodes = expandNode(parent_node, hashMap)
        for i in expanded_nodes:
            # For Tile heuristic
            if algooption == 2:
                i.heuristic = misplacedTiles(i, goal_state)
            # For Manhattan heuristic
            elif algooption == 3:
                i.heuristic = calculate_manhattan(i, goal_state)
            queue.append(i)
            hashMap.append(i.state)
            number_of_nodes_expanded += 1


def expandNode(input_nodes, hashMap):
    # Find the position of 0 value and then move it in all possible directions.
    # Store all possible states/children nodes in a list.
    children = []
    # Logic to move up and down is to change the rows in a matrix. To move left and right change the column value.
    # Up,down,left,right is implemented using the above logic with list of lists.
    # Deep-copy is used to preserve the original state of the node
    expand_node = input_nodes.state
    # Move-down
    move_down = copy.deepcopy(expand_node)
    for row_index, row_value in enumerate(move_down):
        if 0 in row_value:
            indexOfZero = row_value.index(0)
            if row_index != 2:
                # swap of the 0 with the tile below it
                move_down[row_index][indexOfZero], move_down[row_index + 1][indexOfZero] = move_down[row_index + 1][indexOfZero],move_down[row_index][indexOfZero]
                new_node = node(move_down)
                new_node.depth = input_nodes.depth + 1
                if new_node.state not in hashMap:
                    children.append(new_node)
                break

    # Move-Up
    move_up = copy.deepcopy(expand_node)
    for row_index, row_value in enumerate(move_up):
        if 0 in row_value:
            indexOfZero = row_value.index(0)
            if row_index != 0:
                move_up[row_index][indexOfZero], move_up[row_index - 1][indexOfZero] = move_up[row_index - 1][indexOfZero], move_up[row_index][indexOfZero]
                new_node = node(move_up)
                new_node.depth = input_nodes.depth + 1
                if new_node.state not in hashMap:
                    children.append(new_node)
                break

    # Move_left
    move_left = copy.deepcopy(expand_node)
    for row_index, row_value in enumerate(move_left):
        if 0 in row_value:
            indexOfZero = row_value.index(0)
            if indexOfZero != 0:
                move_left[row_index][indexOfZero - 1], move_left[row_index][indexOfZero] = move_left[row_index][indexOfZero], move_left[row_index][indexOfZero - 1]
                new_node = node(move_left)
                new_node.depth = input_nodes.depth + 1
                if new_node.state not in hashMap:
                    children.append(new_node)
                break

    # Move_right
    move_right = copy.deepcopy(expand_node)
    for row_index, row_value in enumerate(move_right):
        if 0 in row_value:
            indexOfZero = row_value.index(0)
            if indexOfZero != 2:
                move_right[row_index][indexOfZero + 1], move_right[row_index][indexOfZero] = move_right[row_index][indexOfZero], move_right[row_index][indexOfZero + 1]
                new_node = node(move_right)
                new_node.depth = input_nodes.depth + 1
                if new_node.state not in hashMap:
                    children.append(new_node)
                break

    return children

# This function calculates the number of misplaced tiles
def misplacedTiles(currentNode, goal_state):
    countOfMisplace = 0
    for x in range(3):
        for y in range(3):
            if currentNode.state[x][y] != goal_state[x][y] and currentNode.state[x][y] != 0:
                countOfMisplace += 1
    return countOfMisplace

# To calculate manhattan distance
def calculate_manhattan(currentNode, goal_state):
    hops = 0
    gridValue = [1, 2, 3, 4, 5, 6, 7, 8]
    for val in gridValue:
        for x in range(3):
            for y in range(3):
                if val == goal_state[x][y]:
                    row1, col1 = x, y
                if val == currentNode.state[x][y]:
                    row2, col2 = x, y
        hops += abs(row1 - row2) + abs(col1 - col2)
    return hops

if __name__ == "__main__":
    main()

