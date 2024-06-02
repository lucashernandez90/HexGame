import numpy as np
import random

class HexBoard:
    def __init__(self, size=11):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]

    def print_board(self):
        print('   ' + '  🔵' * self.size)
        for i in range(self.size):
            print(' ' * (3 * i + 3), end='')
            print('🔴', end='')
            for j in range(self.size):
                if j == self.size - 1:
                    print(f' {self.board[i][j]}', end='')
                else:
                    print(f' {self.board[i][j]} -', end='')
            print(' 🔴')
        print(' ' * (3 * self.size + 4), end='')
        print('  ' + '  🔵' * self.size)

    def is_valid_move(self, row, col):
        if 0 <= row < self.size and 0 <= col < self.size:
            if self.board[row][col] == ' ':
                return True
            else:
                print(f"Tentativa de colocar peça na posição ({row}, {col}) já ocupada.")
                return False
        else:
            print(f"Tentativa de colocar peça fora dos limites do tabuleiro ({row}, {col}).")
            return False

    def place_piece(self, i, j, symbol):
        print(f"Tentando colocar {symbol} em ({i}, {j})")
        if self.is_valid_move(i, j):
            self.board[i][j] = symbol
            print(f"Peça {symbol} colocada em ({i}, {j}) com sucesso.")
            return True
        else:
            print(f"Falha ao tentar colocar {symbol} em ({i}, {j}).")
            return False

    def get_winner(self):
        for i in range(self.size):
            if self.board[i][0] == 'X':
                visited = set()
                if self.dfs((i, 0), visited, 'X', 'right'):
                    return 'X'
        for j in range(self.size):
            if self.board[0][j] == 'O':
                visited = set()
                if self.dfs((0, j), visited, 'O', 'down'):
                    return 'O'
        return None

    def dfs(self, position, visited, player_symbol, direction):
        row, col = position
        if direction == 'down' and row == self.size - 1:
            return True
        if direction == 'right' and col == self.size - 1:
            return True

        visited.add(position)
        for neighbor in self.get_neighbors(position):
            if neighbor not in visited and self.board[neighbor[0]][neighbor[1]] == player_symbol:
                if self.dfs(neighbor, visited, player_symbol, direction):
                    return True
        return False

    def get_neighbors(self, position):
        row, col = position
        directions = [(0, -1), (-1, 0), (-1, 1), (0, 1), (1, 0), (1, -1)]
        neighbors = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.size and 0 <= c < self.size:
                neighbors.append((r, c))
        return neighbors


class Player:
    def __init__(self, symbol):
        self.symbol = symbol


class HexQLearningAI:
    def __init__(self, player, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1): 
        #learning rate: controla o quanto os novos valores de Q substituem os antigos
        #discount factor: determina o peso das recompensas futuras
        #exploratio rate: determina a probalidade de o agente escolher uma acao aleatoria 
        self.player = player
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = {}  # Tabela Q para armazenar os valores de Q

    def get_state_key(self, game):
        return str(game.board)

    def get_action(self, game):
        state_key = self.get_state_key(game)
        if np.random.uniform(0, 1) < self.exploration_rate or state_key not in self.q_table:
            return self.get_blocking_move(game) or (np.random.randint(game.size), np.random.randint(game.size))
        else:
            return max(self.q_table[state_key], key=self.q_table[state_key].get)

    def update_q_table(self, state_key, action, reward, next_state_key):
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = {}

        current_q_value = self.q_table[state_key].get(action, 0)
        max_future_q = max(self.q_table[next_state_key].values()) if self.q_table[next_state_key] else 0
        new_q_value = current_q_value + self.learning_rate * (reward + self.discount_factor * max_future_q - current_q_value)
        self.q_table[state_key][action] = new_q_value

    def make_move(self, game):
        state_key = self.get_state_key(game)
        action = self.get_action(game)
        i, j = action
        reward = self.calculate_reward(game)
        game.place_piece(i, j, self.player.symbol)
        next_state_key = self.get_state_key(game)
        self.update_q_table(state_key, action, reward, next_state_key)

    def calculate_reward(self, game):
        reward = 0
        opponent_symbol = 'X' if self.player.symbol == 'O' else 'O'
        if self.check_winning_move(game):
            reward += 7000
        elif self.check_winning_move(game, opponent_symbol):
            reward -= 15000
        reward += self.evaluate_progress(game)
        reward += self.evaluate_blocks(game, opponent_symbol)
        reward += self.evaluate_strategic_position(game)
        return reward

    def evaluate_progress(self, game):
        progress_reward = 0
        progress_reward += self.count_connected_pieces(game, self.player.symbol) * 10
        return progress_reward

    def count_connected_pieces(self, game, symbol):
        count = 0
        visited = set()
        for i in range(game.size):
            for j in range(game.size):
                if game.board[i][j] == symbol and (i, j) not in visited:
                    count += self.dfs_count(game, i, j, visited, symbol)
        return count

    def dfs_count(self, game, i, j, visited, symbol):
        stack = [(i, j)]
        count = 0
        while stack:
            ci, cj = stack.pop()
            if (ci, cj) not in visited and game.board[ci][cj] == symbol:
                visited.add((ci, cj))
                count += 1
                for di, dj in [(0, 1), (1, 0), (1, 1), (0, -1), (-1, 0), (-1, -1)]:
                    ni, nj = ci + di, cj + dj
                    if 0 <= ni < game.size and 0 <= nj < game.size:
                        stack.append((ni, nj))
        return count

    def evaluate_blocks(self, game, opponent_symbol):
        block_reward = 0
        for i in range(game.size):
            for j in range(game.size):
                if game.board[i][j] == ' ' and self.blocks_opponent(game, i, j, opponent_symbol):
                    block_reward += 9500
        return block_reward

    def evaluate_strategic_position(self, game):
        strategic_score = 0
        for i in range(game.size):
            for j in range(game.size):
                if game.board[i][j] == self.player.symbol:
                    strategic_score += self.evaluate_strategic_position_for_piece(game, i, j)
        return strategic_score

    def evaluate_strategic_position_for_piece(self, game, i, j):
        strategic_score = 0
        directions = [(0, 1), (1, 0), (1, 1), (0, -1), (-1, 0), (-1, -1)]
        priority_directions = [(1, 0), (-1, 0)] if self.player.symbol == 'O' else [(0, 1), (0, -1)]
        for dr, dc in directions:
            r, c = i + dr, j + dc
            if 0 <= r < game.size and 0 <= c < game.size:
                if game.board[r][c] == self.player.symbol:
                    strategic_score += 3000
                    if (dr, dc) in priority_directions:
                        strategic_score += 8000
                elif game.board[r][c] == ' ':
                    r2, c2 = r + dr, c + dc
                    if 0 <= r2 < game.size and 0 <= c2 < game.size and game.board[r2][c2] == self.player.symbol:
                        strategic_score += 6000
        return strategic_score

    def blocks_opponent(self, game, row, col, opponent_symbol):
        game.board[row][col] = opponent_symbol
        if self.check_winning_move(game, opponent_symbol):
            game.board[row][col] = ' '
            return True
        game.board[row][col] = ' '
        return False

    def check_winning_move(self, game, symbol=None):
        symbol = symbol or self.player.symbol
        return game.get_winner() == symbol

    def get_blocking_move(self, game):
        opponent_symbol = 'X' if self.player.symbol == 'O' else 'O'
        for i in range(game.size):
            for j in range(game.size):
                if game.board[i][j] == ' ' and self.blocks_opponent(game, i, j, opponent_symbol):
                    return (i, j)
        return None


# Função principal para executar o jogo
def jogar_hex():
    print("Bem-vindo ao jogo de Hex!")
    tamanho = int(input("Digite o tamanho do tabuleiro (ex: 11 para 11x11): "))
    jogo = HexBoard(tamanho)
    jogo.print_board()
    jogador1 = Player('X')
    jogador2 = Player('O')
    ai = HexQLearningAI(jogador2)  # AI joga como jogador 2 (O)

    jogador_atual = jogador1

    while not jogo.get_winner():
        if jogador_atual == jogador1:
            linha = int(input("Digite a linha para jogar: "))
            coluna = int(input("Digite a coluna para jogar: "))
            if jogo.place_piece(linha, coluna, jogador_atual.symbol):
                jogador_atual = jogador2
        else:
            print("AI está fazendo sua jogada...")
            ai.make_move(jogo)
            jogador_atual = jogador1

        jogo.print_board()

    vencedor = jogo.get_winner()
    if vencedor:
        print(f"Jogador {vencedor} venceu!")
    else:
        print("Não houve vencedor!")

if __name__ == "__main__":
    jogar_hex()
