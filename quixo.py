import math
import time
#Adler Antonio Calvillo Arellano
#Jared López García

class Quixo:
    def __init__(self):
         # Inicializa un tablero de 5x5 lleno de espacios vacíos y establece el jugador actual en 'X'
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        self.current_player = 'X'
        self.side = 'X'

    def print_board(self):
        # Imprime el estado actual del tablero
        for row in self.board:
            print('  |  '.join(row))
            print('---' * 9)

    def is_valid_move(self, row, col):
        #Verifica que el movimiento sea válido (la pieza debe estar en el borde y ser vacía o del jugador actual)
        if row == 0 or row == 4 or col == 0 or col == 4:
            if self.board[row][col] == ' ' or self.board[row][col] == self.current_player:
                return True
        return False

    def is_corner(self, row, col):
        #Devuelve True si es que el movmiento es una de las 4 esquinas del tablero
        return (row == 0 and col == 0) or (row == 0 and col == 4) or (row == 4 and col == 0) or (row == 4 and col == 4)

    def make_move(self, row, col, movement, player):
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
        self.board[row][col] = player
        if movement == "right":  # Desplazamiento a la derecha
            for i in range(col, 4):
                self.board[row][i] = self.board[row][i + 1]  # Desplaza las piezas hacia la izquierda
            self.board[row][4] = player  # Coloca la pieza en la nueva posición
        elif movement == "left":  # Desplazamiento a la izquierda
            for i in range(col, 0, -1):
                self.board[row][i] = self.board[row][i - 1]  # Desplaza las piezas hacia la derecha
            self.board[row][0] = player  # Coloca la pieza en la nueva posición
        elif movement == "down":  # Desplazamiento hacia abajo
            for i in range(row, 4):
                self.board[i][col] = self.board[i + 1][col]  # Desplaza las piezas hacia arriba
            self.board[4][col] = player  # Coloca la pieza en la nueva posición
        elif movement == "up":  # Desplazamiento hacia arriba
            for i in range(row, 0, -1):
                self.board[i][col] = self.board[i - 1][col]  # Desplaza las piezas hacia abajo
            self.board[0][col] = player  # Coloca la pieza en la nueva posición
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
        if self.current_player == 'X':
            for line in lines:
                if all(cell == 'X' for cell in line):
                    return 'X' #Gana el jugador X
            for line in lines:
                if all(cell == 'O' for cell in line):
                    return 'O' #Gana el jugador O
        else:
            for line in lines:
                if all(cell == 'O' for cell in line):
                    return 'O'#El jugador x ha ganado
            for line in lines:
                if all(cell == 'X' for cell in line):
                    return 'X' #El jugador O ha ganado
        return None #No hay ganador aún

    def switch_player(self):
        #Cambia al turno del otro jugador
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def evaluate_board(self, player):
        def count_series(player, length):
            count = 0
            # Evaluar filas
            for row in self.board:
                for i in range(6 - length):
                    if all(cell == player for cell in row[i:i + length]):
                        count += 1
            # Evaluar columnas
            for col in range(5):
                for i in range(6 - length):
                    if all(self.board[j][col] == player for j in range(i, i + length)):
                        count += 1
            # Evaluar diagonales principales y anti-diagonales
            for start in range(5 - length + 1):
                # Principal
                if all(self.board[start + j][start + j] == player for j in range(length)):
                    count += 1
                # Anti-diagonal
                if all(self.board[start + j][4 - (start + j)] == player for j in range(length)):
                    count += 1

            return count

        # Control del centro
        def center_control(player):
            center = self.board[2][2]
            return 3 if center == player else 0

        X_score = (1000 * count_series('X', 5) + 100 * count_series('X', 4) +
                10 * count_series('X', 3) + 1 * count_series('X', 2) + center_control('X'))

        O_score = (1000 * count_series('O', 5) + 100 * count_series('O', 4) +
                10 * count_series('O', 3) + 1 * count_series('O', 2) + center_control('O'))


        # Si el jugador ya ha ganado, devuelve un puntaje alto.
        if count_series(player, 5) > 0:
            return float('inf') if player == 'X' else float('-inf')

        if player == 'X':
            return X_score - O_score
        else:
            return O_score - X_score
        

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

        # Función que implementa el algoritmo Minimax con poda alfa-beta
    def minimax_alpha_beta(self, depth, is_maximizing, alpha, beta):
        # Comprobar si el juego ha terminado y devolver el valor de la posición
        if depth == 0 or self.check_winner() is not None:
            return self.evaluate_board('X')

        if is_maximizing:  # Si es el turno del maximizador (jugador 'O')
            best_value = -math.inf  # Inicializar el mejor puntaje como menos infinito
            # Recorrer todas las celdas del tablero
            for row, col, movement in self.get_possible_moves():
                board_state = self.board[row][col]
                if self.make_move(row, col, movement, 'X'):
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
                if self.make_move(row, col, movement, 'O'):
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

        if self.side == 'O':
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


    def play(self):
        print("Quixo IA")
        print("Seleccione un modo de juego:")
        print("1. Jugar contra otro jugador")
        print("2. Jugar contra la computadora")
        while True:
            mode = input("Ingresa el número correspondiente al modo de juego: ")
            
            if not mode.isdigit():
                continue
            if mode >= '1' and mode <= '2':
                break
            
        if mode == '2':
            player = input("¿Con qué quieres jugar? Escoge 'O' o 'X'")
            while player != 'O' and player != 'X':
                player = input("Seleccione una ficha válida.")
            self.side = player
            

        turn = input("¿Cuál jugador va primero? Escoge 'O' o 'X'")
        while turn != 'O' and turn != 'X':
            turn = input("¿Cuál jugador va primero? Escoge 'O' o 'X'")
        
        self.current_player = turn
                

        # Bucle que controla el flujo del juego
        while True:
            self.print_board()  # Imprime el estado actual del tablero
            print(f"Turno del jugador {self.current_player}")
            if self.current_player == 'X':
                if mode == '1':  # Modo 1v1
                    while True:
                        entrada = input("Ingrese la fila y columna para colocar una pieza (0-4): ")
                        partes = entrada.split()
                        
                        # Verificamos si se ingresaron exactamente dos partes
                        if len(partes) != 2:
                            print("Por favor, ingrese exactamente dos números separados por un espacio.")
                            continue
                        
                        try:
                            # Intentamos convertir las partes a enteros
                            row, col = map(int, partes)
                        except ValueError:
                            print("Por favor, ingrese solo números enteros.")
                            continue
                        
                        # Verificamos si los números están dentro del rango permitido
                        if 0 <= row <= 4 and 0 <= col <= 4:
                            break
                        else:
                            print("Por favor, ingrese números entre 0 y 4.")

                    print(f"Fila seleccionada: {row}, Columna seleccionada: {col}")

                    # Solicita al jugador la nueva fila y columna para colocar su pieza
                    movement = input("Ingrese el movimiento a realizar ('left', 'right', 'up' o 'down'): ")
                    while movement not in ["left", "right", "up", "down"]:
                        movement = input("Ingrese un movimiento valido: ")
                    if self.make_move(row, col, movement, self.current_player):  # Intenta realizar el movimiento
                        winner = self.check_winner()  # Verifica si hay un ganador
                        if winner:
                            self.print_board()
                            print(f"¡El jugador {winner} gana!")
                            break
                        self.switch_player()  # Cambia al siguiente jugador
                    else:
                        print("Movimiento inválido, inténtelo de nuevo.")
                else:  # Modo 1vCPU
                    if self.side == 'X':
                        while True:
                            entrada = input("Ingrese la fila y columna para colocar una pieza (0-4): ")
                            partes = entrada.split()
                            
                            # Verificamos si se ingresaron exactamente dos partes
                            if len(partes) != 2:
                                print("Por favor, ingrese exactamente dos números separados por un espacio.")
                                continue
                            
                            try:
                                # Intentamos convertir las partes a enteros
                                row, col = map(int, partes)
                            except ValueError:
                                print("Por favor, ingrese solo números enteros.")
                                continue
                            
                            # Verificamos si los números están dentro del rango permitido
                            if 0 <= row <= 4 and 0 <= col <= 4:
                                break
                            else:
                                print("Por favor, ingrese números entre 0 y 4.")

                        print(f"Fila seleccionada: {row}, Columna seleccionada: {col}")

                        # Solicita al jugador la nueva fila y columna para colocar su pieza
                        movement = input("Ingrese el movimiento a realizar ('left', 'right', 'up' o 'down'): ")
                        while movement not in ["left", "right", "up", "down"]:
                            movement = input("Ingrese un movimiento valido: ")
                        if self.make_move(row, col, movement, self.current_player):  # Intenta realizar el movimiento
                            winner = self.check_winner()  # Verifica si hay un ganador
                            if winner:
                                self.print_board()
                                print(f"¡El jugador {winner} gana!")
                                break
                            self.switch_player()  # Cambia al siguiente jugador
                        else:
                            print("Movimiento inválido, inténtelo de nuevo.")
                    else:
                        print("Turno de la computadora")
                        start_time = time.time()
                        best_move = self.find_best_move()
                        if best_move:
                            row, col, movement, player = best_move
                            if self.make_move(row, col, movement, player):
                                winner = self.check_winner()
                                if winner:
                                    self.print_board()
                                    print(f"¡El jugador {winner} gana!")
                                    break
                                print(f"La computadora ha hecho su movimiento en la casilla ({best_move[0]}, {best_move[1]}) hacia {best_move[2]}")
                            self.switch_player()
                        else:
                            print("La computadora no puede realizar ningún movimiento. ¡El juego termina en empate!")
                            break
                        end_time = time.time()
                        print(end_time - start_time)
            else:
                if mode == '1':  # Modo 1v1
                    while True:
                        entrada = input("Ingrese la fila y columna para colocar una pieza (0-4): ")
                        partes = entrada.split()
                        
                        # Verificamos si se ingresaron exactamente dos partes
                        if len(partes) != 2:
                            print("Por favor, ingrese exactamente dos números separados por un espacio.")
                            continue
                        
                        try:
                            # Intentamos convertir las partes a enteros
                            row, col = map(int, partes)
                        except ValueError:
                            print("Por favor, ingrese solo números enteros.")
                            continue
                        
                        # Verificamos si los números están dentro del rango permitido
                        if 0 <= row <= 4 and 0 <= col <= 4:
                            break
                        else:
                            print("Por favor, ingrese números entre 0 y 4.")

                    print(f"Fila seleccionada: {row}, Columna seleccionada: {col}")

                    # Solicita al jugador la nueva fila y columna para colocar su pieza
                    movement = input("Ingrese el movimiento a realizar ('left', 'right', 'up' o 'down'): ")
                    while movement not in ["left", "right", "up", "down"]:
                        movement = input("Ingrese un movimiento valido: ")
                    if self.make_move(row, col, movement, self.current_player):  # Intenta realizar el movimiento
                        winner = self.check_winner()  # Verifica si hay un ganador
                        if winner:
                            self.print_board()
                            print(f"¡El jugador {winner} gana!")
                            break
                        self.switch_player()  # Cambia al siguiente jugador
                    else:
                        print("Movimiento inválido, inténtelo de nuevo.")
                else:
                    if self.side == 'O':
                        while True:
                            entrada = input("Ingrese la fila y columna para colocar una pieza (0-4): ")
                            partes = entrada.split()
                            
                            # Verificamos si se ingresaron exactamente dos partes
                            if len(partes) != 2:
                                print("Por favor, ingrese exactamente dos números separados por un espacio.")
                                continue
                            
                            try:
                                # Intentamos convertir las partes a enteros
                                row, col = map(int, partes)
                            except ValueError:
                                print("Por favor, ingrese solo números enteros.")
                                continue
                            
                            # Verificamos si los números están dentro del rango permitido
                            if 0 <= row <= 4 and 0 <= col <= 4:
                                break
                            else:
                                print("Por favor, ingrese números entre 0 y 4.")

                        print(f"Fila seleccionada: {row}, Columna seleccionada: {col}")

                        # Solicita al jugador la nueva fila y columna para colocar su pieza
                        movement = input("Ingrese el movimiento a realizar ('left', 'right', 'up' o 'down'): ")
                        while movement not in ["left", "right", "up", "down"]:
                            movement = input("Ingrese un movimiento valido: ")
                        if self.make_move(row, col, movement, self.current_player):  # Intenta realizar el movimiento
                            winner = self.check_winner()  # Verifica si hay un ganador
                            if winner:
                                self.print_board()
                                print(f"¡El jugador {winner} gana!")
                                break
                            self.switch_player()  # Cambia al siguiente jugador
                        else:
                            print("Movimiento inválido, inténtelo de nuevo.")
                    else:
                        print("Turno de la computadora")
                        start_time = time.time()
                        best_move = self.find_best_move()
                        if best_move:
                            row, col, movement, player = best_move
                            if self.make_move(row, col, movement, player):
                                winner = self.check_winner()
                                if winner:
                                    self.print_board()
                                    print(f"¡El jugador {winner} gana!")
                                    break
                                print(f"La computadora ha hecho su movimiento en la casilla ({best_move[0]}, {best_move[1]}) hacia {best_move[2]}")
                            self.switch_player()
                        else:
                            print("La computadora no puede realizar ningún movimiento. ¡El juego termina en empate!")
                            break
                        end_time = time.time()
                        print(end_time - start_time)

# Inicia el juego
if __name__ == "__main__":
    game = Quixo() 
    game.play()


#Permiti que se pueda jugar tanto con maximizador como minimizador, cambiando los false de is maximizing predeterminados
#Corregi un error en minimax, que hacia que no se actualizara al maximizador o minimizador
#Cambie la funcion makemove para que tambien tome jugador como parametro, y asi poder usar mejor el escoger fichas y cambio de jugador en minimax
#Problema con undomove corregido, jugar contra la ia ya funciona