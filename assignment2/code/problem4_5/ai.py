from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        #TODO: complete this
        if not self.children:
            return True
        else:
            return False


# AI agent. To be used to determine a promising next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # recursive function to build a game tree
    def build_tree(self, node=None, depth=0, ec=False):
        if node == None:
            node = self.root

        if depth == self.search_depth: 
            return 

        if node.player_type == MAX_PLAYER:
            # TODO: find all children resulting from 
            # all possible moves (ignore "no-op" moves)

            # NOTE: the following calls may be useful:
            # self.simulator.reset(*(node.state))
            # self.simulator.get_state()
            # self.simulator.move(direction)

            # get the initial game state (tile matrix and current game score) for resetting later
            # init_game_state = self.simulator.get_state()
            init_game_state = node.state
            init_tile_matrix, init_game_score = init_game_state

            for key, val in MOVES.items():
                # take the action corresponding to the potential pressed key (up, left, down, right)
                has_moved = self.simulator.move(key)

                if has_moved:
                    # get the game state (tile matrix and updated score) after taking the action
                    modified_game_state = self.simulator.get_state()
                    modified_tile_matrix, modified_score = modified_game_state

                    # create a child node with updated game state and the CHANCE player
                    child_node = Node(modified_game_state, CHANCE_PLAYER)

                    # add the child node as a child of current node
                    node.children.append((key, child_node))

                    # recursively build the tree starting from child node
                    self.build_tree(child_node, depth + 1)

                    # reset the game to the state as it was before making the potential move
                    self.simulator.reset(init_tile_matrix, init_game_score)
                else:
                    # create a child node with init game state and no children i.e, leaf node
                    child_node = Node((init_tile_matrix, -100), CHANCE_PLAYER)

                    # add the child node (or leaf/terminal node) as a child of current node
                    node.children.append((key, child_node))


        elif node.player_type == CHANCE_PLAYER:
            # TODO: find all children resulting from 
            # all possible placements of '2's
            # NOTE: the following calls may be useful
            # (in addition to those mentioned above):
            # self.simulator.get_open_tiles():

            # get the initial game state (tile matrix and game score) for resetting later
            # init_game_state = self.simulator.get_state()
            init_game_state = node.state
            init_tile_matrix, init_game_score = init_game_state

            # find all the open/empty tiles in the current game state
            open_tiles_lst = self.simulator.get_open_tiles()
            num_open_tiles = len(open_tiles_lst)

            for idx in open_tiles_lst:
                tm = copy.deepcopy(init_tile_matrix)

                tm[idx[0]][idx[1]] = 2
                modified_game_state = (tm, init_game_score)

                # create a child node with updated game state and the MAX player
                child_node = Node(modified_game_state, MAX_PLAYER)

                # add the child node as a child of current node
                node.children.append((idx, child_node))

                # recursively build the tree starting from child node
                self.build_tree(child_node, depth + 1)

                # reset the game to the state as it was before making the potential move
                self.simulator.reset(init_tile_matrix, init_game_score)

        # TODO: build a tree for each child of this node

    # expectimax implementation; 
    # returns a (best direction, best value) tuple if node is a MAX_PLAYER
    # and a (None, expected best value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same
        # return random.randint(0, 3), 0

        if node == None:
            node = self.root

        if node.is_terminal():
            # TODO: base case
            return None, node.state[1]

        elif node.player_type == MAX_PLAYER:
            # TODO: MAX_PLAYER logic
            # find all the children of the current node
            child_nodes = node.children
            num_child_nodes = len(child_nodes)

            max_score = 0
            optimal_direction = 0

            for i in range(num_child_nodes):
                _, score = self.expectimax(child_nodes[i][1])
                direction = child_nodes[i][0]

                if score > max_score:
                    max_score = score
                    optimal_direction = direction

            return optimal_direction, max_score


        elif node.player_type == CHANCE_PLAYER:
            # TODO: CHANCE_PLAYER logic
            # find all the children of the current node
            child_nodes = node.children
            num_child_nodes = len(child_nodes)

            sum_score = 0
            for i in range(num_child_nodes):
                _, score = self.expectimax(child_nodes[i][1])
                sum_score += score

            return None, sum_score/num_child_nodes


    def custom_expectimax(self, node = None):
        # TODO: delete this random choice but make sure the return type of the function is the same
        # return random.randint(0, 3), 0

        # print("Inside custom EMAX")
        if node == None:
            node = self.root

        if node.is_terminal():
            # TODO: base case
            node_tile_matrix, node_game_score = node.state

            # find the highest tile
            highest_tile = max(max(row) for row in node_tile_matrix)

            # find the total sum of the tile matrix
            sum_tiles = sum(sum(row) for row in node_tile_matrix)

            # weight matrix
            # CORNER_WEIGHT_MATRIX = [[6,5,4,3],[5,4,3,2],[4,3,2,1],[3,2,1,0]]
            CORNER_WEIGHT_MATRIX = [[16,15,14,13],[9,10,11,12],[8,7,6,5],[1,2,3,4]]
            # CORNER_WEIGHT_MATRIX = [[pow(2,16),pow(2,15),pow(2,14),pow(2,13)],[pow(2,9),pow(2,10),pow(2,11),pow(2,12)],[pow(2,8),pow(2,7),pow(2,6),pow(2,5)],[pow(2,1),pow(2,2),pow(2,3),pow(2,4)]]

            # compute the number of open tiles
            # open_tiles = []
            num_open_tiles = 0
            num_pot_merges = 0
            num_monotonic_dec = 0
            num_monotonic_inc = 0
            corner_score = 0
            penalty = 0

            for i in range(0, 4):
                for j in range(0, 4):
                    if node_tile_matrix[i][j] == 0:
                        # open_tiles.append((i, j))
                        num_open_tiles += 1

                    if j > 0:
                        if node_tile_matrix[i][j-1] == node_tile_matrix[i][j]:
                            num_pot_merges += 1

                        if node_tile_matrix[i][j-1] > node_tile_matrix[i][j]:
                            num_monotonic_dec += 1
                        elif node_tile_matrix[i][j-1] < node_tile_matrix[i][j]:
                            num_monotonic_inc += 1

                    if i > 0:
                        if node_tile_matrix[i-1][j] == node_tile_matrix[i][j]:
                            num_pot_merges += 1
                        
                        if node_tile_matrix[i-1][j] > node_tile_matrix[i][j]:
                            num_monotonic_dec += 1
                        elif node_tile_matrix[i-1][j] < node_tile_matrix[i][j]:
                            num_monotonic_inc += 1

                    corner_score += CORNER_WEIGHT_MATRIX[i][j]*node_tile_matrix[i][j]


                    if j > 0:
                        penalty += abs(node_tile_matrix[i][j] - node_tile_matrix[i][j-1])
                    if i > 0:
                        penalty += abs(node_tile_matrix[i][j] - node_tile_matrix[i-1][j])
                    if i < 3:
                        penalty += abs(node_tile_matrix[i][j] - node_tile_matrix[i+1][j])
                    if j < 3:
                        penalty += abs(node_tile_matrix[i][j] - node_tile_matrix[i][j+1])

            # heuristics
            GAME_SCORE_WEIGHT = 2
            SUM_TILE_WEIGHT = 0
            OPEN_TILE_WEIGHT = 800
            POT_MERGE_WEIGHT = 500
            MAX_TILE_WEIGHT = 10
            MONOTONIC_SCORE = 0
            CORNER_WEIGHT = 0
            PENALTY_WEIGHT = 0

            custom_score = (GAME_SCORE_WEIGHT*node_game_score + 
                            SUM_TILE_WEIGHT*sum_tiles +
                            MAX_TILE_WEIGHT*highest_tile + 
                            OPEN_TILE_WEIGHT*num_open_tiles + 
                            POT_MERGE_WEIGHT*num_pot_merges -
                            MONOTONIC_SCORE*min(num_monotonic_inc, num_monotonic_dec) +
                            CORNER_WEIGHT*corner_score -
                            PENALTY_WEIGHT*penalty
                            )
            
            # print(SUM_TILE_WEIGHT*sum_tiles, OPEN_TILE_WEIGHT*num_open_tiles, POT_MERGE_WEIGHT*num_pot_merges, CORNER_WEIGHT*corner_score)
            # custom_score = 0.2*highest_tile + 0.4*num_open_tiles*1000 + 0.4*num_pot_merges*1000
            # assert(custom_score > 0)
            return None, custom_score

        elif node.player_type == MAX_PLAYER:
            # print("Inside custom MAX")
            # TODO: MAX_PLAYER logic
            # find all the children of the current node
            child_nodes = node.children
            num_child_nodes = len(child_nodes)

            max_score = 0
            optimal_direction = 0

            for i in range(num_child_nodes):
                _, score = self.custom_expectimax(child_nodes[i][1])
                direction = child_nodes[i][0]

                if score > max_score:
                    max_score = score
                    optimal_direction = direction

            return optimal_direction, max_score


        elif node.player_type == CHANCE_PLAYER:
            # TODO: CHANCE_PLAYER logic
            # find all the children of the current node
            child_nodes = node.children
            num_child_nodes = len(child_nodes)

            sum_score = 0
            for i in range(num_child_nodes):
                _, score = self.custom_expectimax(child_nodes[i][1])
                sum_score += score

            return None, sum_score/num_child_nodes


    # Do not modify this function
    def compute_decision(self):
        self.build_tree()
        direction, _ = self.expectimax(self.root)
        return direction

    # Implement expectimax with customized evaluation function here
    def compute_decision_ec(self):
        # TODO delete this
        # return random.randint(0, 3)
        # print("Inside custom Expectimax")
        self.build_tree()

        # Modified Expectimax Algorithm that returns the direction
        direction, _ = self.custom_expectimax(self.root)
        return direction
