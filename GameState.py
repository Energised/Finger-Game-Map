#!/usr/local/bin/python3
# GameState.py
#
# Class to store information about the current game state, including:
#   -> Number of players in the game
#   -> List of player objects
#   -> Whose turn it is
#   -> All states achievable from the current state
#   -> If the current state is a halting state

from Player import *

class GameState:

    def __init__(self, n, *args):
        self.num_of_players = n
        self.players = args
        self.turn = False # False for p1, True for p2
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

    def set_turn(self, t):
        self.turn = t

    def get_current_player(self):
        if self.turn == 0:
            return self.players[0]
        elif self.turn == 1:
            return self.players[1]

    def get_other_player(self):
        if self.turn == 0:
            return self.players[1]
        elif self.turn == 1:
            return self.players[0]

    # will be run within the players operations methods

    def change_turn(self):
        self.turn = not self.turn

    def add_connection(self, state):
        self.connected_states.append(state)

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
        if not self.turn:
            print("Player 1's turn:")
        elif self.turn:
            print("Player 2's turn:")
        for player in self.get_players():
            print(player.player_info())
        print()

if __name__ == "__main__":
    p1 = Player(1,1,1)
    p2 = Player(2,1,1)
    g = GameState(2,p1,p2)
    print("(1) turn counter: " + str(g.get_turn()))
    a = g.get_current_player()
    b = g.get_other_player()
    print("(1) current player pid :" + str(a.get_pid()))
    print("(1) other player pid: " + str(b.get_pid()))
    new_state = a.left_to_left(b,g.get_turn())
    print("(2) turn counter: " + str(new_state.get_turn()))
    c = new_state.get_current_player()
    d = new_state.get_other_player()
    print("(2) current player pid: " + str(c.get_pid()))
    print("(2) other player pid: " + str(d.get_pid()))
    s = c.left_to_left(d,new_state.get_turn())
    print("(3) turn counter: " + str(s.get_turn()))
    e = s.get_current_player()
    f = s.get_other_player()
    print("(3) current player pid: " + str(e.get_pid()))
    print("(3) other player pid: " + str(f.get_pid()))
