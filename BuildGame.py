#!/usr/local/bin/python3
# BuildGame.py
#
# Generates every possible game state and stores them once they've been fully explored
# Represented as a rooted graph where:
#
#   -> A state can perform at most 6 actions:
#       1) left_to_left
#       2) left_to_right
#       3) right_to_left
#       4) right_to_right
#       5) four_split
#       6) two_split
#
#   -> Move can be performed when:
#
#       (1) -> not (current_player.get_left() == 0)
#       (2) -> not (current_player.get_left() == 0)
#       (3) -> not (current_player.get_right() == 0)
#       (4) -> not (current_player.get_right() == 0)
#       (5) -> ((current_player.get_left() == 4) and (current_player.get_right() == 0)) or
#              ((current_player.get_left() == 0) and (current_player.get_right() == 4))
#       (6) -> ((current_player.get_left() == 2) and (current_player.get_right() == 0)) or
#              ((current_player.get_left() == 0) and (current_player.get_right() == 2))
#
#
# PROPERLY DEFINED RUNTHROUGH OF ENTIRE PROGRAM:
#   -> Root state is generated as [1,1] and [1,1]
#   -> Graph object is generated using the root state
#   -> Root state is added into the incomplete states queue
#   -> While the incomplete states queue isn't empty:
#       -> Pop the first state off the queue to be the current state
#       -> For each operation:
#           -> Check if it can be performed on the current state
#           -> If it can then:
#               -> Create a new state where that action took place
#               -> Change the turn counter of the new state to the other player (handled in Player.py)
#               -> Add the new state to the current states list of connected states
#               -> If the new state is a halting state:
#                   -> Add it to the completed states list and use continue keyword
#               -> Add the new state to queue of incomplete states
#           -> Otherwise ignore it
#       -> Current state is added to list of completed states in the graph
#  -> The completed states list will contain every possible game state
#
# -> Graph populated with GameState objects
# -> run_operations(node) where:
#   : node is an instance of GameState
#   : each operation is run over node
#   : run another function to test for a (4 to 2) or a (2 to 1) split
#   : add the new game states
#
# note:
# WILL NEED SOME AUXILLARY RECURSIVE FUNCTION TO HANDLE RUNNING OPERATIONS ON A STATE,
# PULLING THE NEXT STATE FROM THE INCOMPLETE STATES QUEUE AND PASSING THAT BACK INTO THE
# RECURSIVE FUNCTION

from Player import Player
from GameState import GameState

from queue import Queue

class BuildGame:

    def __init__(self, root):
        self.root = root
        self.incomplete_states = Queue()
        self.incomplete_states.put(self.root)
        self.complete_states = []
        while(not(self.incomplete_states.empty())):
            n = self.incomplete_states.get()
            n.print_state()
            self.perform_operations(n)

    def get_root(self):
        return self.root

    def perform_operations(self, n):
        current_player = n.get_current_player()
        other_player = n.get_other_player()
        c_left = current_player.get_left()
        c_right = current_player.get_right()
        turn = n.get_turn()
        if not(c_left == 0):
            l2l = current_player.left_to_left(other_player,turn)
            self.handle_new_state(n, l2l)
            l2r = current_player.left_to_right(other_player,turn)
            self.handle_new_state(n, l2r)
        if not(c_right == 0):
            r2l = current_player.right_to_left(other_player,turn)
            self.handle_new_state(n, r2l)
            r2r = current_player.right_to_right(other_player,turn)
            self.handle_new_state(n, r2r)
        if ((c_left == 4) and (c_right == 0)) or ((c_left == 0) and (c_right == 4)):
            fsp = current_player.four_split(other_player,turn)
            self.handle_new_state(n, fsp)
        if ((c_left == 2) and (c_right == 0)) or ((c_left == 0) and (c_right == 2)):
            tsp = current_player.two_split(other_player,turn)
            self.handle_new_state(n, tsp)
        self.complete_states.append(n)
        print("Completed the state")

    def handle_new_state(self, parent, state):
        parent.add_connection(state) # connect parent and child states
        if(state.is_end_state()): # check for halting state
            self.complete_states.append(state)
        else:
            self.incomplete_states.put(state)

if __name__ == "__main__":
    p1 = Player(1,1,1) # create players
    p2 = Player(2,1,1)
    g = GameState(2,p1,p2) # add them to the root state
    b = BuildGame(g)
    #b.get_root().print_state()
