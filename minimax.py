import random


class HexMinimaxAI:
    def __init__(self, player):
        self.player = player

    def make_move(self, game):
        best_move = self.get_best_move(game)
        if best_move is not None:
            game.make_move_position(best_move)

    def get_best_move(self, game, depth=5):
        if game.total_moves == 0:
            return self.get_random_move(game)

        # Bloquear ponte dupla se houver uma oportunidade
        for blocking_move in game.valid_moves():
            if self.block_double_bridge(game):
                return blocking_move

        # Verificar se há uma oportunidade de criar uma ponte dupla
        for double_bridge_move in game.valid_moves():
            if self.is_double_bridge(game, double_bridge_move):
                return double_bridge_move

        # Verificar se o jogador humano está prestes a formar uma conexão entre os lados opostos
        for move in game.valid_moves():
            if self.is_connecting_move(game, move, game.players[game.current_player.opposite()].symbol):
                return move

        # Priorizar movimentos que bloqueiam as possíveis conexões do jogador humano
        for move in game.valid_moves():
            if self.blocks_opponent_connection(game, move):
                return move

        # Se nenhuma jogada prioritária for encontrada, usar o algoritmo minimax
        evaluation, best_move = self.minimax(game, depth, float('-inf'), float('inf'), True)
        
        if best_move is None:
            # Se nenhum movimento válido for encontrado, retornar um movimento padrão aleatório
            return self.get_random_move(game)
        else:
            return best_move

    def is_connecting_move(self, game, move, opponent_symbol):
        row, col = move
        # Verificar se a jogada do jogador humano está se aproximando de formar uma conexão entre os lados opostos
        if opponent_symbol == 'X':
            if row == game.size - 1:  # Se a jogada estiver na borda inferior do tabuleiro
                return True
        else:
            if col == game.size - 1:  # Se a jogada estiver na borda direita do tabuleiro
                return True
        return False

    def blocks_opponent_connection(self, game, move):
        row, col = move
        opponent_symbol = game.players[game.current_player.opposite()].symbol
        return (opponent_symbol == 'X' and row == game.size - 1) or (opponent_symbol == 'O' and col == game.size - 1)

    def get_random_move(self, game, exclude_start=False):
        valid_moves = game.valid_moves()
        if exclude_start:
            valid_moves = [move for move in valid_moves if move != (0, 0)]
        return random.choice(valid_moves) if valid_moves else None

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.is_game_over():
            return self.assess(game.current_player), None

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.get_valid_moves_without_blocking(game):
                new_game = game.copy_game()
                new_game.make_move(move)
                eval, _ = self.minimax(new_game, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.get_valid_moves_without_blocking(game):
                new_game = game.copy_game()
                new_game.make_move(move)
                eval, _ = self.minimax(new_game, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_valid_moves_without_blocking(self, game):
        valid_moves = []
        for move in game.valid_moves():
            if not self.has_piece_in_front(game, move):
                valid_moves.append(move)
        return valid_moves

    def has_piece_in_front(self, game, move):
        row, col = move
        player_symbol = game.current_player.symbol
        if player_symbol == 'X':
            return row == 0 or (col > 0 and game.board[row][col - 1] != '.')
        else:
            return col == 0 or (row > 0 and game.board[row - 1][col] != '.')

    def assess(self, player):
        opponent_symbol = player.opposite().symbol
        player_pieces = 0
        opponent_pieces = 0

        # Contagem do número de peças para cada jogador no tabuleiro
        for i in range(player.game.size):
            for j in range(player.game.size):
                if player.game.board[i][j] == player.symbol:
                    player_pieces += 1
                elif player.game.board[i][j] == opponent_symbol:
                    opponent_pieces += 1

        # Avaliação com base na diferença de peças
        evaluation = player_pieces - opponent_pieces

        # Avaliação extra: considerar a proximidade das peças do jogador às bordas opostas
        edge_bonus = 0
        max_distance = max(player.game.size // 2, player.game.size - player.game.size // 2 - 1)  # Distância máxima da borda ao centro do tabuleiro
        for i in range(player.game.size):
            for j in range(player.game.size):
                if player.game.board[i][j] == player.symbol:
                    # Calcular a distância até a borda oposta mais próxima
                    distance_to_opposite_edge = min(i, player.game.size - i - 1, j, player.game.size - j - 1)
                    # Subtrair a distância da distância máxima e adicionar ao bônus
                    edge_bonus += max_distance - distance_to_opposite_edge

        # Adiciona o bônus da proximidade às bordas opostas à avaliação
        evaluation += edge_bonus

        return evaluation

    def is_double_bridge(self, game, move):
        row, col = move
        player_symbol = game.current_player.symbol
        if player_symbol == 'X' and row > 1 and game.board[row-1][col] == player_symbol and game.board[row-2][col] == player_symbol:
            return True
        elif player_symbol == 'O' and col > 1 and game.board[row][col-1] == player_symbol and game.board[row][col-2] == player_symbol:
            return True
        return False

    def block_double_bridge(self, game):
        for move in game.valid_moves():
            if self.is_double_bridge(game, move):
                return True
        return False
