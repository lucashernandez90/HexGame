import pygame
from pygame.locals import *
from game import Game, Player
from minimax import HexMinimaxAI
from enum import Enum
import sys

class Circles(Enum):
    X = '🔴'
    O = '🔵'
    E = " "  # empty

class HexBoard:
    def __init__(self, size):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]

    def print_board(self):
        # Imprime a linha superior com as bordas do jogador 🔵
        print('   ' + '  🔵' * self.size)

        for i in range(self.size):
            # Imprime os espaços à esquerda
            print(' ' * (3 * i + 3), end='')

            # Imprime a borda esquerda do jogador 🔴
            print('🔴', end='')
            for j in range(self.size):
                if j == self.size - 1:
                    print(f' {self.board[i][j]}', end='')
                else:
                    print(f' {self.board[i][j]} -', end='')  # Adiciona o separador '-'

            # Imprime a borda direita do jogador 🔴
            print(' 🔴')

        # Imprime os espaços à esquerda para a linha inferior
        print(' ' * (3 * self.size + 4), end='')

        # Imprime a linha inferior com as bordas do jogador 🔵
        print('  ' + '  🔵' * self.size)

    def is_valid_move(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == ' '

    def place_piece(self, row, col, piece):
        if self.is_valid_move(row, col):
            self.board[row][col] = piece
            return True
        else:
            return False

    def get_winner(self, player_symbol):
        visited = set()
        for j in range(self.size):
            if self.board[0][j] == player_symbol and self.dfs((0, j), visited, player_symbol, 'right'):
                return player_symbol
        visited = set()
        for i in range(self.size):
            if self.board[i][0] == player_symbol and self.dfs((i, 0), visited, player_symbol, 'down'):
                return player_symbol
        return None



def escolher_simbolo():
    while True:
        symbol = input("Escolha o símbolo para o jogador (X ou O): ").upper()
        if symbol == 'X' or symbol == 'O':
            return symbol
        else:
            print("Entrada inválida. Por favor, escolha 'X' ou 'O'.")

def iniciar_jogo():
    print("Bem-vindo ao Hex!")
    symbol_x = escolher_simbolo()
    symbol_o = 'X' if symbol_x == 'O' else 'O'

    player_x = Player(symbol_x)
    player_o = Player(symbol_o)

    # Criando o objeto Game
    size = 11  # Definindo o tamanho do tabuleiro
    game = Game(size, player_x, player_o)

    # Criando o objeto HexBoard
    board = HexBoard(size)
    board.print_board()

    # Escolha do jogador AI
    ai_player = player_o if symbol_x == 'X' else player_x
    print("Jogador AI:", ai_player.symbol)
    ai_symbol = ai_player.symbol

    # Determinar o símbolo da IA com base na escolha do jogador humano
    if symbol_x == 'O':
        ai_symbol = Circles.X.value  # A IA escolhe o símbolo oposto ao jogador humano
    else:
        ai_symbol = Circles.O.value  # A IA escolhe o símbolo oposto ao jogador humano

    # Criar o jogador da IA com o símbolo determinado
    ai_player = Player(ai_symbol)

    # Instanciar a classe HexMinimaxAI
        # Configurar a IA com o jogador criado
    ai_instance = HexMinimaxAI(ai_player)

    # Loop do jogo
    while not game.is_game_over():
        # Jogada do jogador humano
        move = input("Digite a linha e coluna para a sua jogada (ex: 3 5): ")
        try:
            row, col = map(int, move.split())
            while not board.is_valid_move(row, col):
                print("Movimento inválido. Tente novamente.")
                move = input("Digite a linha e coluna para a sua jogada (ex: 3 5): ")
                row, col = map(int, move.split())
        except ValueError:
            print("Entrada inválida. Tente novamente.")
            continue
        
        if not board.place_piece(row, col, Circles.X.value):
            print("Movimento inválido. Tente novamente.")
            continue
        
        # Avaliação da posição atual do tabuleiro
        player = game.turn()
        evaluation = game.assess(player)
        print(f"Avaliação da posição para {player.symbol}: {evaluation}")
        
        # Jogada da IA
        best_move = ai_instance.get_random_move(game)
        board.place_piece(*best_move, ai_symbol)
        game.make_move_position(best_move)
        board.print_board()

        # Verifica se a jogada da IA resulta em uma ponte dupla
        ai_instance.is_double_bridge(game, best_move)

    if game.is_game_over():
        winner = board.get_winner(game.current_player.symbol)
        if winner == 'X':
            print("Parabéns! Você venceu!")
        else: 
            print("Você perdeu! A máquina venceu.")


if __name__ == "__main__":
    iniciar_jogo()
