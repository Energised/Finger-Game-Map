#!/usr/local/bin/python3
# test.py
#
# messing about designing program for finger game
#
# ATTRIBUTES
#   n -> number of players (allow it to generate for 2+ players)
#   L -> [p1_left, p2_left] -> number of fingers on each hand
#   R -> [p1_right, p2_right] -> as above
#
#
# action will edit the EDIT: now just ints containing the current number of fingers on each hand
# possible moves
#
# for player 0:
#   L[0] -> L[1] - left_to_left()
#   L[0] -> R[1] - left_to_right()
#   R[0] -> L[1] - right_to_left()
#   R[0] -> R[1] - right_to_right()
#
# for player 1:
#   L[1] -> L[0]
#   L[1] -> R[0]
#   R[1] -> L[0]
#   R[1] -> R[0]
#
# FOR SPLITTING MOVES:
#
#   L[0] -> L[0] AND R[0]
#   R[0] -> L[0] AND R[0]
#
#   :: Will need 2 functions:
#       1) four_split()
#       2) two_split()
#
# -> GameState holds the number of players and a list of Player instances
# -> Player holds the number of fingers on each hand and handles state changes
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
#               -> Change the turn counter of the new state to the other player
#               -> Add the new state to the current states list of connected states
#               -> If the new state is a halting state:
#                   -> Add it to the completed states list and use continue keyword
#               -> Add the new state to queue of incomplete states
#           -> Otherwise ignore it
#       -> Current state is added to list of completed states in the graph
#  -> The completed states list will contain every possible game state
#

class GameState:

    def __init__(self, n, *args):
        self.num_of_players = n
        self.players = args
        self.turn = 0 # 0 for player 1, 1 for player 2
        self.connected_states = [] # list of states achievable from itself
        self.end_state = self.state_check()

    def get_num_of_players(self):
        return self.num_of_players

    def get_players(self): # returns list of players
        return self.players

    def gen_players(self): # returns players individually
        for player in self.get_players():
            yield player

    def get_turn(self):
        return self.turn

    # will be run within the players operations methods

    def change_turn(self):
        self.turn = int(not self.get_turn())

    def is_end_state(self):
        return self.end_state

    def state_check(self):
        end_state = False
        for player in self.gen_players():
            if ((player.get_left() == 0) and (player.get_right() == 0)):
                end_state = True
            else:
                continue
        return end_state

    def print_state(self):
        #print("Players: " + str(self.get_num_of_players()))
        if self.turn == 0:
            print("Player 1's turn:")
        elif self.turn == 1:
            print("Player 2's turn:")
        for player in self.get_players():
            print(player.player_info())
        print()

# Class to store information about some Player within the game
#   DATA: Number of fingers on each hand
#   OPERATIONS: All possible moves a player could make
# (need to decide where to have restrictions on when a split can be made)

class Player:

    def __init__(self, pid, left, right):
        self.left = left
        self.right = right
        self.pid = pid

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_pid(self):
        return self.pid

    def set_left(self, value):
        self.left = value

    def set_right(self, value):
        self.right = value

    def set_pid(self, value):
        self.pid = value

    def gen_new_state(self, player_to_old, new_left, new_right):
        if self.pid == 1:
            player_to_new = Player(2, new_left, new_right)
            next_state = GameState(2, self, player_to_new)
        elif self.pid == 2:
            player_to_new = Player(1, new_left, new_right)
            next_state = GameState(2, player_to_new, self)
        next_state.change_turn()
        return next_state

    def left_to_left(self, player_to_old):
        new_left = player_to_old.get_left() + self.get_left()
        new_right = player_to_old.get_right()
        next_state = self.gen_new_state(player_to_old, new_left, new_right)
        print("\nPlayer " + str(self.get_pid()) + ": LEFT TO LEFT\n")
        #next_state.print_state()
        return next_state

    def left_to_right(self, player_to_old):
        new_left = player_to_old.get_left()
        new_right = player_to_old.get_right() + self.get_left()
        next_state = self.gen_new_state(player_to_old, new_left, new_right)
        print("\nPlayer " + str(self.get_pid()) + ": LEFT TO RIGHT\n")
        #next_state.print_state()
        return next_state

    def right_to_left(self, player_to_old):
        new_right = player_to_old.get_right()
        new_left = player_to_old.get_left() + self.get_right()
        next_state = self.gen_new_state(player_to_old, new_left, new_right)
        print("\nPlayer " + str(self.get_pid()) + ": RIGHT TO LEFT\n")
        #next_state.print_state()
        return next_state

    def right_to_right(self, player_to_old):
        new_right = player_to_old.get_right() + self.get_right()
        new_left = player_to_old.get_left()
        next_state = self.gen_new_state(player_to_old, new_left, new_right)
        print("\nPlayer " + str(self.get_pid()) + ": RIGHT TO RIGHT\n")
        #next_state.print_state()
        return next_state

    def four_split(self, other_player):
        new_left, new_right = 2, 2
        player_self_new = Player(self.get_pid(), new_left, new_right)
        if self.pid == 1:
            next_state = GameState(2,player_self_new, other_player)
        elif self.pid == 2:
            next_state = GameState(2, other_player, player_self_new)
        next_state.change_turn()
        return next_state

    def two_split(self, other_player):
        new_left, new_right = 1, 1
        player_self_new = Player(self.get_pid(), new_left, new_right)
        if self.pid == 1:
            next_state = GameState(2, player_self_new, other_player)
        elif self.pid == 2:
            next_state = GameState(2, other_player, player_self_new)
        next_state.change_turn()
        return next_state

    def player_info(self):
        return "Player " + str(self.get_pid()) + " = [L = " + str(self.get_left()) + ", R = " + str(self.get_right()) + "]"

def main():
    p1 = Player(1,1,1)
    p2 = Player(2,1,1)
    #print(p1.pid, " : Player 1")
    #print(p2.pid, " : Player 2")
    #print(p1.get_left())
    g = GameState(2,p1,p2)
    #g.print_state()
    players = g.get_players() # return the ordered list of players (MUST BE ORDERED, BEAR IN MIND)
    next_state = players[0].left_to_left(players[1]) # make a move, return new state
    print("FIRST STATE:")
    g.print_state()
    print("\nSECOND STATE:")
    next_state.print_state()
    #g.print_state()

def halt_test():
    p1 = Player(1,3,2)
    p2 = Player(2,0,0)
    g = GameState(2,p1,p2)
    print(g.is_end_state())

def four_split_test():
    p1 = Player(1,4,0)
    p2 = Player(2,3,1)
    g = GameState(2,p1,p2)
    print("FIRST STATE:")
    g.print_state()
    players = g.get_players()
    new_state = players[0].four_split(players[1])
    print("SECOND STATE:")
    new_state.print_state()

def two_split_test():
    p1 = Player(1,2,0)
    p2 = Player(2,3,1)
    g = GameState(2,p1,p2)
    print("FIRST STATE:")
    g.print_state()
    players = g.get_players()
    new_state = players[0].two_split(players[1])
    print("SECOND STATE:")
    new_state.print_state()

if __name__ == "__main__":
    main()
    halt_test()
    four_split_test()
    two_split_test()
