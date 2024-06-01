import math
#Adler Antonio Calvillo Arellano
#Jared López García

class Quixo:
    def __init__(self):
         # Inicializa un tablero de 5x5 lleno de espacios vacíos y establece el jugador actual en 'X'
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        self.current_player = 'X'
        self.side = 'X' # Sirve para que el codigo play identifique con que pieza juega el jugador y con que la AI

    def print_board(self):
        # Imprime el estado actual del tablero
        for row in self.board:
            print('  |  '.join(row))
            print('---' * 9)

    def is_valid_move(self, row, col):
        if row == 0 or row == 4 or col == 0 or col == 4:
            if self.board[row][col] == ' ' or self.board[row][col] == self.current_player:
                return True
        return False

    def is_corner(self, row, col):
        return (row == 0 and col == 0) or (row == 0 and col == 4) or (row == 4 and col == 0) or (row == 4 and col == 4)

    def make_move(self, row, col, movement, player):
        if not self.is_valid_move(row, col):
            print("Asegúrese de tomar una pieza que esté en los bordes.")
            return False

        if self.is_corner(row, col):
            if (row == 0 and col == 0 and movement not in ['right', 'down']) or \
               (row == 0 and col == 4 and movement not in ['left', 'down']) or \
               (row == 4 and col == 0 and movement not in ['right', 'up']) or \
               (row == 4 and col == 4 and movement not in ['left', 'up']):
                print("Movimiento inválido para una esquina.")
                return False
        else:          
            if (row == 0 and movement == 'up') or (row == 4 and movement == 'down') or \
               (col == 0 and movement == 'left') or (col == 4 and movement == 'right'):
                print("Asegúrese de colocar la pieza en un lugar diferente al que la tomó.")
                return False

        self.board[row][col] = player
        if movement == "right":
            for i in range(col, 4):
                self.board[row][i] = self.board[row][i + 1]
            self.board[row][4] = player
        elif movement == "left":
            for i in range(col, 0, -1):
                self.board[row][i] = self.board[row][i - 1]
            self.board[row][0] = player
        elif movement == "down":
            for i in range(row, 4):
                self.board[i][col] = self.board[i + 1][col]
            self.board[4][col] = player
        elif movement == "up":
            for i in range(row, 0, -1):
                self.board[i][col] = self.board[i - 1][col]
            self.board[0][col] = player
        return True

    def check_winner(self):
        lines = []
        for row in self.board:
            lines.append(row)
        for col in range(5):
            lines.append([self.board[row][col] for row in range(5)])
        lines.append([self.board[i][i] for i in range(5)])
        lines.append([self.board[i][4-i] for i in range(5)])

        if self.current_player == 'X':
            for line in lines:
                if all(cell == 'X' for cell in line):
                    return 'X'
            for line in lines:
                if all(cell == 'O' for cell in line):
                    return 'O'
        else:
            for line in lines:
                if all(cell == 'O' for cell in line):
                    return 'O'
            for line in lines:
                if all(cell == 'X' for cell in line):
                    return 'X'
        return None

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def evaluate_board(self, symbol):
        def evaluate_line(line, symbol, opponent):
            if symbol * 5 in line:
                return 100000
            elif opponent * 5 in line:
                return -100000
            else:
                player_score = len([cell for cell in line if cell == symbol])
                opponent_score = len([cell for cell in line if cell == opponent])
                return 5 * player_score - 3 * opponent_score

        def center_control(board, symbol):
            center_value = 10
            center_positions = [(1, 1), (1, 3), (3, 1), (3, 3)]
            score = 0
            if board[2][2] == symbol:
                score += center_value * 3
            for pos in center_positions:
                if board[pos[0]][pos[1]] == symbol:
                    score += center_value
            return score

        def count_patterns(pattern):
            count = 0
            # Evaluar filas
            for row in self.board:
                row_str = ''.join(map(str, row))
                count += row_str.count(pattern)
            # Evaluar columnas
            for col in range(5):
                col_str = ''.join(str(self.board[j][col]) for j in range(5))
                count += col_str.count(pattern)
            # Evaluar diagonales principales y anti-diagonales
            diag1 = ''.join(str(self.board[i][i]) for i in range(5))
            diag2 = ''.join(str(self.board[i][4 - i]) for i in range(5))
            count += diag1.count(pattern)
            count += diag2.count(pattern)
            return count

        if count_patterns(str(symbol) * 5) > 0:
            return 100000000
        if symbol == 'X':
            opponent = 'O'
        else:
            opponent = 'X'
        score = 0

        for i in range(5):
            row = self.board[i]
            column = [self.board[j][i] for j in range(5)]
            score += evaluate_line(row, symbol, opponent)
            score += evaluate_line(column, symbol, opponent)

        diag1 = [self.board[i][i] for i in range(5)]
        diag2 = [self.board[i][4 - i] for i in range(5)]
        score += evaluate_line(diag1, symbol, opponent)
        score += evaluate_line(diag2, symbol, opponent)

        score += center_control(self.board, symbol)

        score += 10 * count_patterns(str(symbol) * 3)  # Tres en línea del jugador
        score += 20 * count_patterns(str(symbol) * 4)  # Cuatro en línea del jugador
        score -= 5 * count_patterns(str(opponent) * 3)  # Penalizar tres en línea del oponente
        score -= 10 * count_patterns(str(opponent) * 4)  # Penalizar cuatro en línea del oponente

        return score

    def get_possible_moves(self):
        moves = []
        for row in range(5):
            for col in range(5):
                if self.is_valid_move(row, col):
                    if row == 0:
                        moves.append((row, col, 'down'))
                        if col == 0 or col == 4:
                            moves.append((row, col, 'right' if col == 0 else 'left'))
                    elif row == 4:
                        moves.append((row, col, 'up'))
                        if col == 0 or col == 4:
                            moves.append((row, col, 'right' if col == 0 else 'left'))
                    if col == 0:
                        moves.append((row, col, 'right'))
                    elif col == 4:
                        moves.append((row, col, 'left'))
        return moves
    
    """
    EXPERIMENTO
    def negamax_alpha_beta(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.check_winner() is not None:
            return self.evaluate_board()

        best_value = float('-inf') if maximizing_player else float('inf')
        for row, col, movement in self.get_possible_moves():
            self.make_move(row, col, movement)
            value = -self.negamax_alpha_beta(depth - 1, -beta, -alpha, not maximizing_player)
            self.undo_move(row, col, movement)

            if maximizing_player:
                best_value = max(best_value, value)
                alpha = max(alpha, value)
            else:
                best_value = min(best_value, value)
                beta = min(beta, value)

            if alpha >= beta:
                break

        return best_value

    """

    def minimax_alpha_beta(self, depth, is_maximizing, alpha, beta):
        if depth == 0 or self.check_winner() is not None:
            return self.evaluate_board('X')

        if is_maximizing:
            best_value = -math.inf
            for row, col, movement in self.get_possible_moves():
                board_state = self.board[row][col]
                if self.make_move(row, col, movement, 'X'):
                    value = self.minimax_alpha_beta(depth-1, False, alpha, beta)
                    self.undo_move(row, col, movement, board_state)
                    best_value = max(value, best_value)
                    alpha = max(alpha, best_value)
                    if beta <= alpha:
                        break
            return best_value
        else:
            best_value = math.inf
            for row, col, movement in self.get_possible_moves():
                board_state = self.board[row][col]
                if self.make_move(row, col, movement, 'O'):
                    value = self.minimax_alpha_beta(depth-1, True, alpha, beta)
                    self.undo_move(row, col, movement, board_state)
                    best_value = min(value, best_value)
                    beta = min(value, best_value)
                    if beta <= alpha:
                        break
            return best_value


    def find_best_move(self):
        best_move = ()
        max_value = -math.inf
        min_value = math.inf
        alpha = -math.inf
        beta = math.inf

        if self.current_player == 'X':
            is_maximizing = False

            for row, col, movement in self.get_possible_moves():
                board_state = self.board[row][col]
                if self.make_move(row, col, movement, 'X'):
                    value = self.minimax_alpha_beta(2, is_maximizing, alpha, beta)
                    self.undo_move(row, col, movement, board_state)

                    if value > max_value:
                        max_value = value
                        best_move = (row, col, movement, 'X')

        else:
            is_maximizing = True
            for row, col, movement in self.get_possible_moves():
                board_state = self.board[row][col]
                if self.make_move(row, col, movement, 'O'):
                    value = self.minimax_alpha_beta(2, is_maximizing, alpha, beta)
                    self.undo_move(row, col, movement, board_state)

                    if value < min_value:
                        min_value = value
                        best_move = (row, col, movement, 'O')

        return best_move

    def undo_move(self, row, col, movement, board_state):
        if movement == "right":
            self.board[row][4] = board_state
            for i in range(4, col, -1):
                self.board[row][i] = self.board[row][i - 1]
            self.board[row][col] = board_state
        elif movement == "left":
            self.board[row][0] = board_state
            for i in range(0, col):
                self.board[row][i] = self.board[row][i + 1]
            self.board[row][col] = board_state
        elif movement == "down":
            self.board[4][col] = board_state
            for i in range(4, row, -1):
                self.board[i][col] = self.board[i - 1][col]
            self.board[row][col] = board_state
        elif movement == "up":
            self.board[0][col] = board_state
            for i in range(0, row):
                self.board[i][col] = self.board[i + 1][col]
            self.board[row][col] = board_state