import math
import os

#Adler Antonio Calvillo Arellano
#Jared López García
        
class Quixo:
    def __init__(self):
         # Inicializa un tablero de 5x5 lleno de espacios vacíos y establece el jugador actual en 'X'
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        self.current_player = 'x'
        self.side = 'x'

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
        if self.current_player == 'x':
            for line in lines:
                if all(cell == 'x' for cell in line):
                    return 'X' #Gana el jugador X
            for line in lines:
                if all(cell == 'o' for cell in line):
                    return 'O' #Gana el jugador O
        else:
            for line in lines:
                if all(cell == 'o' for cell in line):
                    return 'O'#El jugador x ha ganado
            for line in lines:
                if all(cell == 'x' for cell in line):
                    return 'X' #El jugador O ha ganado
        return None #No hay ganador aún

    def switch_player(self):
        #Cambia al turno del otro jugador
        self.current_player = 'o' if self.current_player == 'x' else 'x'

    def evaluate_board(self, player):
        def count_series(player, length):
            count = 0
            for row in self.board:
                for i in range(6 - length):
                    if all(cell == player for cell in row[i:i + length]):
                        count += 1
            for col in range(5):
                for i in range(6 - length):
                    if all(self.board[j][col] == player for j in range(i, i + length)):
                        count += 1
            for i in range(6 - length):
                if all(self.board[i + j][i + j] == player for j in range(length)):
                    count += 1
                if all(self.board[i + j][4 - i - j] == player for j in range(length)):
                    count += 1
            return count

        X_score = (1000 * count_series('x', 5) + 100 * count_series('x', 4) + 
                10 * count_series('x', 3) + 1 * count_series('x', 2))
        
        O_score = (1000 * count_series('o', 5) + 100 * count_series('o', 4) + 
                10 * count_series('o', 3) + 1 * count_series('o', 2))

        if player == 'x':
            return X_score - O_score
        else:
            return -O_score + X_score
        

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
            return self.evaluate_board('x')

        if is_maximizing:  # Si es el turno del maximizador (jugador 'O')
            best_value = -math.inf  # Inicializar el mejor puntaje como menos infinito
            # Recorrer todas las celdas del tablero
            for row, col, movement in self.get_possible_moves():
                board_state = self.board[row][col]
                if self.make_move(row, col, movement, 'x'):
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
                if self.make_move(row, col, movement, 'o'):
                    value = self.minimax_alpha_beta(depth-1, True, alpha, beta)
                    self.undo_move(row, col, movement, board_state)
                    best_value = min(value, best_value)  # Actualizar el mejor puntaje
                    beta = min(value, best_value)  # Actualizar beta
                    if beta <= alpha:  # Poda alfa
                        break  # Salir del bucle si ya no es necesario evaluar más movimientos
            return best_value  # Devolver el mejor puntaje encontrado



    def find_best_move(self):
        best_move = ()
        best_value = -math.inf
        alpha = -math.inf
        beta = math.inf

        if self.side == 'x':
            is_maximizing = False
        else:
            is_maximizing = True

        for row, col, movement in self.get_possible_moves():
            board_state = self.board[row][col]
            if self.make_move(row, col, movement, self.current_player):
                value = self.minimax_alpha_beta(2, is_maximizing, alpha, beta)
                self.undo_move(row, col, movement, board_state)

                if value > best_value:
                    best_value = value
                    best_move = (row, col, movement, self.current_player)

        return best_move
    
    def find_blocking_move(self, opponent):
        for row, col, movement in self.get_possible_moves():
            board_state = [row[:] for row in self.board]
            if self.make_move(row, col, movement, opponent):
                if self.check_winner() == opponent.upper():
                    self.board = board_state
                    return (row, col, movement, self.current_player)
                self.board = board_state
        return None


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
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\t\t\033[1;34mQuixo IA\033[0m\n")
        print("\033[1m Seleccione un modo de juego: \033[0m")
        print("\033[1;32m 1. Jugar contra otro jugador \033[0m")
        print("\033[1;32m 2. Jugar contra la computadora \033[0m")
        count = 1
        draw = 101
        while True:
            mode = input("\n\033[1m Ingresa el número correspondiente al modo de juego: \033[0m")
            
            if not mode.isdigit():
                continue
            if mode >= '1' and mode <= '2':
                break
            
        if mode == '2':
            player = input("¿Con qué quieres jugar? Escoge 'O' o 'X'\n").lower()
            while player != 'o' and player != 'x':
                player = input("Seleccione una ficha válida.").lower()
            self.side = player
            

        turn = input("¿Cuál jugador va primero? Escoge 'O' o 'X'\n").lower()
        while turn != 'o' and turn != 'x':
            turn = input("¿Cuál jugador va primero? Escoge 'O' o 'X'\n").lower()
        
        self.current_player = turn
                

        # Bucle que controla el flujo del juego
        while True:
            if count == draw:
                print("Límite de turnos alcanzado.\nEmpate")
                break
            
            self.print_board()  # Imprime el estado actual del tablero
            if count != 0:
                print(f"Turno {count}")
                
            print(f"Turno del jugador {self.current_player}")
            
            if self.current_player == 'x':
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
                    if count == draw:
                            print("Límite de turnos alcanzado.\nEmpate")
                            break
                        
                    if self.side == 'x':
                        if count == draw:
                            print("Límite de turnos alcanzado.\nEmpate")
                            break
                        
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
                        movement = input("Ingrese el movimiento a realizar ('left', 'right', 'up' o 'down'): ").lower()
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
                        count += 1
                        #block_move = self.find_blocking_move('x' if self.current_player == 'o' else 'o')
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
            else:
                if mode == '1':  # Modo 1v1
                    if count == draw:
                        print("Límite de turnos alcanzado.\nEmpate")
                        break
                    
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
                    movement = input("Ingrese el movimiento a realizar ('left', 'right', 'up' o 'down'): ").lower()
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
                    if self.side == 'o':
                        if count == draw:
                            print("Límite de turnos alcanzado.\nEmpate")
                            break
                        
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
                        movement = input("Ingrese el movimiento a realizar ('left', 'right', 'up' o 'down'): ").lower()
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
                        count += 1
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


                          


class QuixoBot:
    # symbol sera un numero representando el simbolo con el que me
    # toca jugar. Puede tener el valor 1 o -1;
    def __init__(self, symbol):
        # define a name for your bot to appear during the log printing.
        self.name = "Invincibot"
        self.quixo_instance = Quixo()
        self.symbol = symbol
        

    # board es el estado actual del tablero. Sera una matriz de 5x5 que contiene
    # los siguientes numeros enteros.
    #  0 - blank cubit
    #  1 - X cubit
    # -1 - O cubit
    def play_turn(self, board):
        # Esta funcion debe tomar el tablero actual, simular el movimiento deseado
        # y regresarlo al evaluador.
        # return new_board
        simulated_board = [row[:] for row in board]
        best_move = self.find_best_move(simulated_board)
        if best_move:
            row, col, movement, player = best_move
            self.quixo_instance.make_move(row, col, movement, player)
            return self.quixo_instance.board
        
        return board

    def find_best_move(self, board):
        best_move = ()
        best_value = -math.inf
        alpha = -math.inf
        beta = math.inf

        is_maximizing = self.symbol == 1

        for row, col, movement in self.quixo_instance.get_possible_moves(board):
            board_state = board[row][col]
            board[row][col] = self.symbol
            value = self.minimax_alpha_beta(2, is_maximizing, alpha, beta, board)
            board[row][col] = board_state

            if value > best_value:
                best_value = value
                best_move = (row, col, movement, self.symbol)

        return best_move

    def minimax_alpha_beta(self, depth, is_maximizing, alpha, beta, board):
        if depth == 0 or self.quixo_instance.check_winner(board) is not None:
            return self.quixo_instance.evaluate_board(self.symbol, board)

        if is_maximizing:
            best_value = -math.inf
            for row, col, movement in self.quixo_instance.get_possible_moves(board):
                board_state = board[row][col]
                board[row][col] = self.symbol
                value = self.minimax_alpha_beta(depth - 1, False, alpha, beta, board)
                board[row][col] = board_state
                best_value = max(value, best_value)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value
        else:
            best_value = math.inf
            for row, col, movement in self.quixo_instance.get_possible_moves(board):
                board_state = board[row][col]
                opponent = -1 if self.symbol == 1 else 1
                board[row][col] = opponent
                value = self.minimax_alpha_beta(depth - 1, True, alpha, beta, board)
                board[row][col] = board_state
                best_value = min(value, best_value)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value




    # Esta funcion sera llamada antes de empezar una nueva partida,
    # por lo que su proposito es resetear cualquier estado que sea necesario
    # para empezar desde 0.
    # Tambien recibe el nuevo simbolo con el que empezara la partida.
    def reset(self, symbol):
        self.__init__(symbol)
    


# Inicia el juego
if __name__ == "__main__":
    game = Quixo() 
    game.play()
    #game = QuixoBot("x")
    #game.play_turn()


#solo esqueleto del bot del profe
#nombre que impone
#Adaptación de metodos para el bot, probablemene no sea eficiente aún
