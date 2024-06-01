import math
import copy

class QuixoBot2:
    # symbol sera un numero representando el simbolo con el que me
    # toca jugar. Puede tener el valor 1 o -1
    def __init__(self, symbol):
        # define a name for your bot to appear during the log printing.
        self.name = "Blue Suit InvinciBot"
        self.symbol = symbol
        self.board = [[0] * 5 for _ in range(5)]

    def print_board(self):
        for row in self.board:
            print(row)

    def is_valid_move(self, row, col):
        #Verifica que el movimiento sea válido (la pieza debe estar en el borde y ser vacía o del jugador actual)
        if row == 0 or row == 4 or col == 0 or col == 4:
            if self.board[row][col] == 0 or self.board[row][col] == self.symbol:
                return True
        return False

    def is_corner(self, row, col):
        #Devuelve True si es que el movmiento es una de las 4 esquinas del tablero
        return (row == 0 and col == 0) or (row == 0 and col == 4) or (row == 4 and col == 0) or (row == 4 and col == 4)

    def make_move(self, row, col, movement, symbol):
        # Verifica el lugar desde el que se toma la pieza es válido
        if not self.is_valid_move(row, col):
            print("Asegúrese de tomar una pieza que esté en los bordes.")
            return False    #Movimiento inválido

        # Líneas agregadas: Verificar si la pieza está en una esquina y restringir movimientos
        if self.is_corner(row, col):
            if (row == 0 and col == 0 and movement not in ['right', 'down']) or \
               (row == 0 and col == 4 and movement not in ['left', 'down']) or \
               (row == 4 and col == 0 and movement not in ['right', 'up']) or \
               (row == 4 and col == 4 and movement not in ['left', 'up']):
                print("Movimiento inválido para una esquina.")
                return False
        else:
            # Movimientos no válidos en bordes que no son esquinas            
            if (row == 0 and movement == 'up') or (row == 4 and movement == 'down') or \
               (col == 0 and movement == 'left') or (col == 4 and movement == 'right'):
                print("Asegúrese de colocar la pieza en un lugar diferente al que la tomó.")
                return False

        #Movimiento válido
        self.board[row][col] = symbol
        if movement == "right":  # Desplazamiento a la derecha
            for i in range(col, 4):
                self.board[row][i] = self.board[row][i + 1]  # Desplaza las piezas hacia la izquierda
            self.board[row][4] = symbol  # Coloca la pieza en la nueva posición
        elif movement == "left":  # Desplazamiento a la izquierda
            for i in range(col, 0, -1):
                self.board[row][i] = self.board[row][i - 1]  # Desplaza las piezas hacia la derecha
            self.board[row][0] = symbol  # Coloca la pieza en la nueva posición
        elif movement == "down":  # Desplazamiento hacia abajo
            for i in range(row, 4):
                self.board[i][col] = self.board[i + 1][col]  # Desplaza las piezas hacia arriba
            self.board[4][col] = symbol  # Coloca la pieza en la nueva posición
        elif movement == "up":  # Desplazamiento hacia arriba
            for i in range(row, 0, -1):
                self.board[i][col] = self.board[i - 1][col]  # Desplaza las piezas hacia abajo
            self.board[0][col] = symbol # Coloca la pieza en la nueva posición
        return True  # Movimiento realizado con éxito

    def check_winner(self):
        #Comprueba si hay ganador
        lines = []
        #Añade todas las filas al conjunto de líneas a verificar
        for row in self.board:
            lines.append(row)
        #Añade todas las columnas al conjunto de filas a verificar
        for col in range(5):
            lines.append([self.board[row][col] for row in range(5)])
        #Añade las diagonales al conjunto de líneas a verificar
        lines.append([self.board[i][i] for i in range(5)])
        lines.append([self.board[i][4-i] for i in range(5)])

        # Comprueba cada línea para ver si hay un ganador
        # En caso de formarse 5 en fila de los dos bandos en una jugada, gana el que hizo la jugada.
        # por ello se revisa primero al current player.
        if self.symbol == 1:
            for line in lines:
                if all(cell == 1 for cell in line):
                    return 1 #Gana el jugador X
            for line in lines:
                if all(cell == -1 for cell in line):
                    return -1 #Gana el jugador O
        else:
            for line in lines:
                if all(cell == -1 for cell in line):
                    return -1#El jugador x ha ganado
            for line in lines:
                if all(cell == 1 for cell in line):
                    return 1 #El jugador O ha ganado
        return None #No hay ganador aún
    
    def evaluate_board(self, symbol):
        opponent = -symbol  # Asume que el símbolo del oponente es la negación del símbolo del bot
        
        def evaluate_line(line, symbol, opponent):
            line_str = ''.join(map(str, line))
            if '00000' in line_str:
                return 0  # Puntaje neutral para una línea vacía
            if str(symbol) * 5 in line_str:
                return 100000  # Puntaje más alto para una línea ganadora
            if str(opponent) * 5 in line_str:
                return -100000  # Puntaje negativo alto para evitar la línea ganadora del oponente
            
            # Configuraciones de peso para patrones en la línea
            score = 0
            patterns = {
                str(symbol) * 4 + '0': 5000,
                '0' + str(symbol) * 4: 5000,
                str(symbol) * 3 + '00': 1000,
                '00' + str(symbol) * 3: 1000,
                str(symbol) * 2 + '000': 100,
                '000' + str(symbol) * 2: 100,
                str(symbol) + '0000': 10,
                '0000' + str(symbol): 10
            }
            
            for pattern, value in patterns.items():
                if pattern in line_str:
                    score += value
            
            #Evaluar los patrones del oponente para bloquearlos
            opponent_patterns = {
                str(opponent) * 4 + '0': -5000,
                '0' + str(opponent) * 4: -5000,
                str(opponent) * 3 + '00': -1000,
                '00' + str(opponent) * 3: -1000,
            }
            
            for pattern, value in opponent_patterns.items():
                if pattern in line_str:
                    score += value
            
            return score
        
        def count_patterns(symbol, length, pattern):
            count = 0
            # Evalua filas
            for row in self.board:
                row_str = ''.join(map(str, row))
                count += row_str.count(pattern)
            # Evalua columnas
            for col in range(5):
                col_str = ''.join(str(self.board[j][col]) for j in range(5))
                count += col_str.count(pattern)
            # Evalua diagonales
            diag1 = ''.join(str(self.board[i][i]) for i in range(5))
            diag2 = ''.join(str(self.board[i][4 - i]) for i in range(5))
            count += diag1.count(pattern)
            count += diag2.count(pattern)
            return count
        
        def center_control(board, symbol):
            center_value = 50  #ajusta el valor segun sea necesario
            center_positions = [(2, 2), (1, 1), (1, 3), (3, 1), (3, 3)]
            score = 0
            for pos in center_positions:
                if board[pos[0]][pos[1]] == symbol:
                    score += center_value
            return score
        
        #evalua todas las linneas del tablero
        lines = []
        #filas y columnas
        for i in range(5):
            lines.append(self.board[i])  # Rows
            column = [self.board[j][i] for j in range(5)]
            lines.append(column)
        
        # diagonales
        diagonals = [
            [self.board[i][i] for i in range(5)],
            [self.board[i][4-i] for i in range(5)]
        ]
        lines.extend(diagonals)
        
        for line in lines:
            score += evaluate_line(line, symbol, opponent)
        
        #Añade un extra score por controlar el centro
        score += center_control(self.board, symbol)
        
        #Añadir puntajes por patrones específicos
        score += 50 * count_patterns(symbol, 3, str(symbol) * 3)  # Three in a row
        score += 100 * count_patterns(symbol, 4, str(symbol) * 4)  # Four in a row
        score -= 25 * count_patterns(opponent, 3, str(opponent) * 3)  # Opponent's three in a row
        score -= 50 * count_patterns(opponent, 4, str(opponent) * 4)  # Opponent's four in a row
        
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
    
        # Función que implementa el algoritmo Minimax con poda alfa-beta
    def minimax_alpha_beta(self, depth, is_maximizing, alpha, beta):
        # Comprobar si el juego ha terminado y devolver el valor de la posición
        if depth == 0 or self.check_winner() is not None:
            return self.evaluate_board(1)

        if is_maximizing:  # Si es el turno del maximizador (jugador 'O')
            best_value = -math.inf  # Inicializar el mejor puntaje como menos infinito
            # Recorrer todas las celdas del tablero
            for row, col, movement in self.get_possible_moves():
                board_state = self.board[row][col]
                if self.make_move(row, col, movement, 1):
                # Llamar recursivamente a minimax_alpha_beta para evaluar la posición después de este movimiento
                    value = self.minimax_alpha_beta(depth-1, False, alpha, beta)
                    self.undo_move(row, col, movement, board_state)
                    best_value = max(value, best_value)  # Actualizar el mejor puntaje
                    alpha = max(alpha, best_value)  # Actualizar alfa
                    if beta <= alpha:  # Poda beta
                        break  # Salir del bucle si ya no es necesario evaluar más movimientos
            return best_value  # Devolver el mejor puntaje encontrado
        else:  # Si es el turno del minimizador (jugador 'X')
            best_value = math.inf  # Inicializar el mejor puntaje como infinito
            # Recorrer todas las celdas del tablero
            for row, col, movement in self.get_possible_moves():
                board_state = self.board[row][col]
                if self.make_move(row, col, movement, -1):
                    value = self.minimax_alpha_beta(depth-1, True, alpha, beta)
                    self.undo_move(row, col, movement, board_state)
                    best_value = min(value, best_value)  # Actualizar el mejor puntaje
                    beta = min(value, best_value)  # Actualizar beta
                    if beta <= alpha:  # Poda alfa
                        break  # Salir del bucle si ya no es necesario evaluar más movimientos
            return best_value  # Devolver el mejor puntaje encontrado



    def find_best_move(self):
        best_move = ()
        max_value = -math.inf
        min_value = math.inf
        alpha = -math.inf
        beta = math.inf

        if self.symbol == 1:
            is_maximizing = False

            for row, col, movement in self.get_possible_moves():
                board_state = self.board[row][col]
                if self.make_move(row, col, movement, 1):
                    value = self.minimax_alpha_beta(2, is_maximizing, alpha, beta)
                    self.undo_move(row, col, movement, board_state)

                    if value > max_value:
                        max_value = value
                        best_move = (row, col, movement, 1)

        else:
            is_maximizing = True
            for row, col, movement in self.get_possible_moves():
                board_state = self.board[row][col]
                if self.make_move(row, col, movement, -1):
                    value = self.minimax_alpha_beta(2, is_maximizing, alpha, beta)
                    self.undo_move(row, col, movement, board_state)

                    if value < min_value:
                        min_value = value
                        best_move = (row, col, movement, -1)

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



    # board es el estado actual del tablero. Sera una matriz de 5x5 que contiene
    # los siguientes numeros enteros.
    #  0 - blank cubit
    #  1 - X cubit
    # -1 - O cubit
    def play_turn(self, board):
        # Esta funcion debe tomar el tablero actual, simular el movimiento deseado
        # y regresarlo al evaluador.
        # return new_board
        self.board = copy.deepcopy(board)
        #self.print_board()
        best_move = self.find_best_move()
        if best_move:
            row, col, movement, symbol = best_move
            self.make_move(row, col, movement, symbol)
            #print(f"La computadora ha hecho su movimiento en la casilla ({best_move[0]}, {best_move[1]}) hacia {best_move[2]}")
            return self.board


    # Esta funcion sera llamada antes de empezar una nueva partida,
    # por lo que su proposito es resetear cualquier estado que sea necesario
    # para empezar desde 0.
    # Tambien recibe el nuevo simbolo con el que empezara la partida.
    def reset(self, symbol):
        self.__init__(symbol)

# Ejemplo de uso
"""
# Creamos el tablero inicial
board = [[0] * 5 for _ in range(5)]
# Inicializamos el bot 
bot = QuixoBot2(1)

# Jugamos un turno con este bot y recibimos el nuevo estado del tablero.
new_board = bot.play_turn(board)
for row in new_board:
    print(row)
"""
