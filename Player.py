#!/usr/local/bin/python3
# Player.py
#
# Class to manage a Player within the game

# Class to store information about some Player within the game
#   DATA: Number of fingers on each hand
#   OPERATIONS: All possible moves a player could make
# (need to decide where to have restrictions on when a split can be made)

from GameState import *

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

    def gen_new_state(self, player_to_old, new_left, new_right, turn):
        if self.pid == 1:
            player_to_new = Player(2, new_left, new_right)
            next_state = GameState(2, self, player_to_new)
        elif self.pid == 2:
            player_to_new = Player(1, new_left, new_right)
            next_state = GameState(2, player_to_new, self)
        next_state.set_turn(turn) # set turn to the previous states turn value
        next_state.change_turn() # then change
        return next_state

    def boundary_check(self, f): # checks if a hand is out
        if f >= 5:
            return 0
        else:
            return f

    def left_to_left(self, player_to_old, turn):
        new_left = self.boundary_check(int(player_to_old.get_left() + self.get_left()))
        new_right = player_to_old.get_right()
        next_state = self.gen_new_state(player_to_old, new_left, new_right, turn)
        print("\nPlayer " + str(self.get_pid()) + ": LEFT TO LEFT")
        #next_state.print_state()
        return next_state

    def left_to_right(self, player_to_old, turn):
        new_left = player_to_old.get_left()
        new_right = self.boundary_check(int(player_to_old.get_right() + self.get_left()))
        next_state = self.gen_new_state(player_to_old, new_left, new_right, turn)
        print("\nPlayer " + str(self.get_pid()) + ": LEFT TO RIGHT")
        #next_state.print_state()
        return next_state

    def right_to_left(self, player_to_old, turn):
        new_right = player_to_old.get_right()
        new_left = self.boundary_check(int(player_to_old.get_left() + self.get_right()))
        print("\nPlayer " + str(self.get_pid()) + ": RIGHT TO LEFT")
        next_state = self.gen_new_state(player_to_old, new_left, new_right, turn)
        #next_state.print_state()
        return next_state

    def right_to_right(self, player_to_old, turn):
        new_right = self.boundary_check(int(player_to_old.get_right() + self.get_right()))
        new_left = player_to_old.get_left()
        next_state = self.gen_new_state(player_to_old, new_left, new_right, turn)
        print("\nPlayer " + str(self.get_pid()) + ": RIGHT TO RIGHT")
        #next_state.print_state()
        return next_state

    def four_split(self, other_player, turn):
        new_left, new_right = 2, 2
        player_self_new = Player(self.get_pid(), new_left, new_right)
        if self.pid == 1:
            next_state = GameState(2,player_self_new, other_player)
        elif self.pid == 2:
            next_state = GameState(2, other_player, player_self_new)
        next_state.set_turn(turn) # set new turn to the previous states turn
        next_state.change_turn() # since this method doesnt use the gen_new_state method it must call this
        print("\nPlayer " + str(self.get_pid()) + ": FOUR SPLIT")
        return next_state

    def two_split(self, other_player, turn):
        new_left, new_right = 1, 1
        player_self_new = Player(self.get_pid(), new_left, new_right)
        if self.pid == 1:
            next_state = GameState(2, player_self_new, other_player)
        elif self.pid == 2:
            next_state = GameState(2, other_player, player_self_new)
        next_state.set_turn(turn) # set new turn to the previous states turn
        next_state.change_turn() # since this method doesnt use the gen_new_state method it must call this
        print("Player " + str(self.get_pid()) + ": TWO SPLIT")
        return next_state

    def player_info(self):
        return "Player " + str(self.get_pid()) + " : [L = " + str(self.get_left()) + ", R = " + str(self.get_right()) + "]"

if __name__ == "__main__":
    p1 = Player(1,3,4)
    p2 = Player(2,2,1)
    g = GameState(2,p1,p2)
    new_state = p1.right_to_left(p2,g.get_turn()) # testing the boundary check function
    new_state.print_state()
