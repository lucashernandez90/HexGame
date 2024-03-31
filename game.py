class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def opposite(self):
        return 'O' if self.symbol == 'X' else 'X'

class Game:
    def __init__(self, size, player_x, player_o):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.players = {player_x.symbol: player_x, player_o.symbol: player_o}
        self.current_player = player_x
        self.total_moves = 0

    def make_move_position(self, move):
        row, col = move
        if self.is_valid_move(row, col):
            self.board[row][col] = self.current_player.symbol
            self.current_player = self.players[self.current_player.opposite()]
            self.total_moves += 1  # Incrementa o contador de movimentos após cada jogada
        else:
            print("Movimento inválido! Tente novamente.")

    def get_total_moves(self):
        return self.total_moves

    def is_valid_move(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == ' '

    def turn(self):
        return self.current_player

    def valid_moves(self):
        moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == ' ':
                    moves.append((i, j))
        return moves

    def is_game_over(self):
        return len(self.valid_moves()) == 0 or self.won()

    def won(self):
        if self.current_player.symbol == 'X':
            for i in range(self.size):
                if self.dfs((i, 0), set(), 'X') and self.dfs((i, self.size - 1), set(), 'X'):
                    return True
        else:
            for i in range(self.size):
                if self.dfs((0, i), set(), 'O') and self.dfs((self.size - 1, i), set(), 'O'):
                    return True
        return False


    def dfs(self, pos, visited, player):
        if pos in visited:
            return False
        visited.add(pos)

        row, col = pos
        if player == 'X' and col == self.size - 1:
            return True
        if player == 'O' and row == self.size - 1:
            return True

        directions = ['right', 'down_right'] if player == 'X' else ['down_right', 'right']
        for direction in directions:
            neighbors = self.get_neighbors(pos, direction)
            for neighbor in neighbors:
                if self.board[neighbor[0]][neighbor[1]] == player:
                    if self.dfs(neighbor, visited, player):
                        return True
        return False

    def get_neighbors(self, pos, direction=None):
        row, col = pos
        neighbors = []
        if row > 0:
            neighbors.append((row - 1, col))
        if row < self.size - 1:
            neighbors.append((row + 1, col))
        if col > 0:
            neighbors.append((row, col - 1))
        if col < self.size - 1:
            neighbors.append((row, col + 1))
        if row > 0 and col < self.size - 1:
            neighbors.append((row - 1, col + 1))
        if row < self.size - 1 and col > 0:
            neighbors.append((row + 1, col - 1))

        # Adiciona a verificação da direção
        if direction == 'right' and col < self.size - 1:
            neighbors.append((row, col + 1))

        return neighbors


    def assess(self, player):
        player_symbol = player.symbol
        opponent_symbol = self.players[player.opposite()].symbol

        player_pieces = 0
        opponent_pieces = 0

        # Contagem do número de peças para cada jogador no tabuleiro
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == player_symbol:
                    player_pieces += 1
                elif self.board[i][j] == opponent_symbol:
                    opponent_pieces += 1

        # Avaliação com base na diferença de peças
        evaluation = player_pieces - opponent_pieces

        # Avaliação extra: considerar a proximidade das peças do jogador às bordas opostas
        edge_bonus = 0
        max_distance = max(self.size // 2, self.size - self.size // 2 - 1)  # Distância máxima da borda ao centro do tabuleiro
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == player_symbol:
                    # Calcular a distância até a borda oposta mais próxima
                    distance_to_opposite_edge = min(i, self.size - i - 1, j, self.size - j - 1)
                    # Subtrair a distância da distância máxima e adicionar ao bônus
                    edge_bonus += max_distance - distance_to_opposite_edge

        # Adiciona o bônus da proximidade às bordas opostas à avaliação
        evaluation += edge_bonus

        return evaluation

    def copy_game(self):
        copied_game = Game(self.size, self.players['X'], self.players['O'])
        copied_game.board = [row[:] for row in self.board]
        copied_game.current_player = self.current_player
        copied_game.players = self.players
        return copied_game
