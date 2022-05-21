#!/usr/bin/env python3

from games import *
import pygame
import sys
import random

class GameOfNim(Game):

    def __init__(self, board):
        """takes the initial board position and creates the initial GameState"""
        avail_moves = list()
        for r in range(len(board)):
            for n in range(1, board[r]+1):
                avail_moves.append((r, n))
        self.initial = GameState(to_move='MAX', utility=0, board=board, moves=avail_moves)

        pygame.init()
        self._screen = pygame.display.set_mode((800,600))
        self._screen.fill((255, 255, 255))
        pygame.display.set_caption("Game of Nim")

        self._matchImg = pygame.image.load('matchstick.png') #<a href="https://www.flaticon.com/free-icons/matchstick" title="matchstick icons">Matchstick icons created by Shastry - Flaticon</a>
        self._matchImg = pygame.transform.scale(self._matchImg, (50, 50))

        self._surface = pygame.display.get_surface()
        self._font = pygame.font.SysFont(None, 50)

        self._rows = len(board)-1
        self._amount = 1

    def actions(self, state):
        """returns a list of valid actions in the given state."""
        return state.moves

    def result(self, state, move):
        """returns the new state reached from the given state and the given move."""
        while move in state.moves:
            new_board = state.board.copy()
            new_board[move[0]] = new_board[move[0]] - move[1]
        
            avail_moves = list()
            for r in range(len(new_board)):
                for n in range(1, new_board[r]+1):
                    avail_moves.append((r, n))
        
            return GameState(to_move=('MIN' if state.to_move == 'MAX' else 'MAX'),
                            utility=1 if state.to_move == 'MAX' else -1 ,board=new_board, moves=avail_moves)
        return state

    def displayboard(self, state):
        pygame.draw.rect(self._screen, (255,255,255), (0,0,800,450))
        self._matchX = 50
        self._matchY = 50
        #self._rows = len(state.board)-1
        for i in range (0, len(state.board)):
            for j in range(0, state.board[i]):
                self._screen.blit(self._matchImg, (self._matchX, self._matchY))
                self._matchX +=70
            self._matchX = 50
            self._matchY += 100
        self._row_text = self._font.render(f"Row: {self._rows+1}", True, (0, 0, 0))
        self._row_textRect = self._row_text.get_rect()
        self._row_textRect.center = (250, 500)
        self._amount_text = self._font.render(f"Amount: {self._amount}", True, (0, 0, 0))
        self._amount_textRect = self._amount_text.get_rect()
        self._amount_textRect.center = (500, 500)
        pygame.display.update()

    def utility(self, state, player):
        """returns +1 if MAX wins, -1 if MIN wins"""
        #self.display(state)
        #print(state.board)
        if player == 'MAX':
            return state.utility
        else: -state.utility

    def terminal_test(self, state):
        """returns True if the given state represents the end of a game"""
        if sum(state.board) == 0:
            return True
        else: False

    def to_move(self, state):
        """Return the player whose move it is in this state."""
        return state.to_move
    
    def play_game(self, *players):
        """Play an n-person, move-alternating game."""
        state = self.initial
        self.displayboard(state)
        idx = 0
        winner = False
        while not winner:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # computer player
                if idx == 0:
                    move = players[idx](self, state)
                    state = self.result(state, move)
                    idx = 1
                    if self.terminal_test(state):
                        idx = 0
                # human player
                elif idx == 1:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self._amount = 1
                            if self._rows > 0:
                                self._rows -= 1
                            else: self._rows = 0
                            self._row_text = self._font.render(f"Row: {self._rows+1}", True, (0, 0, 0))
                        if event.key == pygame.K_DOWN:
                            self._amount = 1
                            if self._rows < len(state.board)-1:
                                self._rows += 1
                            else: self._rows = len(state.board)-1
                            self._row_text = self._font.render(f"Row: {self._rows+1}", True, (0, 0, 0))
                        if event.key == pygame.K_RIGHT:
                            if self._amount < state.board[self._rows]:
                                self._amount += 1
                            elif state.board[self._rows] == 0:
                                self._amount = 0
                            else: self._amount = 1
                            self._amount_text = self._font.render(f"Amount: {self._amount}", True, (0, 0, 0))
                        if event.key == pygame.K_LEFT:
                            if self._amount > 1:
                                self._amount -= 1
                            elif state.board[self._rows] == 0:
                                self._amount = 0
                            else: self._amount = state.board[self._rows]
                            self._amount_text = self._font.render(f"Amount: {self._amount}", True, (0, 0, 0))
                        if event.key == pygame.K_RETURN:
                            if state.board[self._rows] > 0 and state.board[self._rows] >= self._amount:
                                move = eval(f'{self._rows}, {self._amount}')
                                state = self.result(state, move)
                                idx = 0
                                if self.terminal_test(state):
                                    idx = 1

                self.displayboard(state)
                pygame.draw.rect(self._screen, (255,255,255), self._row_textRect)
                self._screen.blit(self._row_text, (self._row_textRect))
                pygame.draw.rect(self._screen, (255,255,255), self._amount_textRect)
                self._screen.blit(self._amount_text, (self._amount_textRect))

                if self.terminal_test(state):
                    self._screen.fill((255, 255, 255))
                    if idx == 0:
                        self._winner_text = self._font.render(f"Computer wins!", True, (0, 0, 0))
                        self._winner_textRect = self._winner_text.get_rect()
                        self._winner_textRect.center = (250, 250)
                        self._screen.blit(self._winner_text, (self._winner_textRect))
        
                    if idx == 1:
                        self._winner_text = self._font.render(f"Human wins!", True, (0, 0, 0))
                        self._screen.blit(self._winner_text, (self._winner_textRect))
                        self._winner_textRect.center = (250, 250)
                        self._screen.blit(self._winner_text, (self._winner_textRect))
                
                pygame.display.update()
     
if __name__ == "__main__":
    #nim = GameOfNim(board=[0, 5, 3, 1])  # Creating the game instance
    nim = GameOfNim(board=[random.randint(1,9), random.randint(1,9), random.randint(1,9), random.randint(1,9)]) # a much larger tree to search
    utility = nim.play_game(alpha_beta_cutoff_player, query_player) # computer moves first
