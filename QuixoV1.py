import math
#Adler Antonio Calvillo Arellano
#Jared López García

class Quixo:
    def __init__(self):
         # Inicializa un tablero de 5x5 lleno de espacios vacíos y establece el jugador actual en 'X'
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        self.current_player = 'X'

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

    def make_move(self, row, col, movement):
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
        self.board[row][col] = self.current_player
        if movement == "right":  # Desplazamiento a la derecha
            for i in range(col, 4):
                self.board[row][i] = self.board[row][i + 1]  # Desplaza las piezas hacia la izquierda
            self.board[row][4] = self.current_player  # Coloca la pieza en la nueva posición
        elif movement == "left":  # Desplazamiento a la izquierda
            for i in range(col, 0, -1):
                self.board[row][i] = self.board[row][i - 1]  # Desplaza las piezas hacia la derecha
            self.board[row][0] = self.current_player  # Coloca la pieza en la nueva posición
        elif movement == "down":  # Desplazamiento hacia abajo
            for i in range(row, 4):
                self.board[i][col] = self.board[i + 1][col]  # Desplaza las piezas hacia arriba
            self.board[4][col] = self.current_player  # Coloca la pieza en la nueva posición
        elif movement == "up":  # Desplazamiento hacia arriba
            for i in range(row, 0, -1):
                self.board[i][col] = self.board[i - 1][col]  # Desplaza las piezas hacia abajo
            self.board[0][col] = self.current_player  # Coloca la pieza en la nueva posición
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

    def evaluate_board(self):
        winner = self.check_winner()
        if winner == 'X':
            return 1
        elif winner == 'O':
            return -1
        return 0

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

    def find_best_move(self):
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for row, col, movement in self.get_possible_moves():
            self.make_move(row, col, movement)
            value = -self.negamax_alpha_beta(3, -beta, -alpha, False)
            self.undo_move(row, col, movement)

            if value > best_value:
                best_value = value
                best_move = (row, col, movement)

        return best_move

    def undo_move(self, row, col, movement):
        if movement == "right":
            self.board[row][4] = ' '
            for i in range(4, col, -1):
                self.board[row][i] = self.board[row][i - 1]
            self.board[row][col] = ' '
        elif movement == "left":
            self.board[row][0] = ' '
            for i in range(0, col):
                self.board[row][i] = self.board[row][i + 1]
            self.board[row][col] = ' '
        elif movement == "down":
            self.board[4][col] = ' '
            for i in range(4, row, -1):
                self.board[i][col] = self.board[i - 1][col]
            self.board[row][col] = ' '
        elif movement == "up":
            self.board[0][col] = ' '
            for i in range(0, row):
                self.board[i][col] = self.board[i + 1][col]
            self.board[row][col] = ' '

    def play(self):
        print("Quixo IA")
        print("Seleccione un modo de juego:")
        print("1. Jugar contra otro jugador")
        print("2. Jugar contra la computadora")
        mode = input("Ingresa el número correspondiente al modo de juego: ")

        # Bucle que controla el flujo del juego
        while True:
            self.print_board()  # Imprime el estado actual del tablero
            print(f"Turno del jugador {self.current_player}")
            if self.current_player == 'X':
                if mode == '1':  # Modo 1v1
                    row, col = map(int, input("Ingrese la fila y columna para recoger una pieza (0-4): ").split())
                    # Solicita al jugador la nueva fila y columna para colocar su pieza
                    movement = input("Ingrese el movimiento a realizar ('left', 'right', 'up' o 'down'): ")
                    while movement not in ["left", "right", "up", "down"]:
                        movement = input("Ingrese un movimiento valido: ")
                    if self.make_move(row, col, movement):  # Intenta realizar el movimiento
                        winner = self.check_winner()  # Verifica si hay un ganador
                        if winner:
                            self.print_board()
                            print(f"¡El jugador {winner} gana!")
                            break
                        self.switch_player()  # Cambia al siguiente jugador
                    else:
                        print("Movimiento inválido, inténtelo de nuevo.")
                elif mode == '2':  # Modo 1vCPU
                    print("Turno de la computadora")
                    best_move = self.find_best_move()
                    if best_move:
                        self.make_move(*best_move)
                        print(f"La computadora ha hecho su movimiento en la casilla ({best_move[0]}, {best_move[1]}) hacia {best_move[2]}")
                        winner = self.check_winner()
                        if winner:
                            self.print_board()
                            print(f"¡El jugador {winner} gana!")
                            break
                        self.switch_player()
                    else:
                        print("La computadora no puede realizar ningún movimiento. ¡El juego termina en empate!")
                        break
                else:
                    print("Modo de juego no válido. Por favor, selecciona 1 o 2.")
            else:
                row, col = map(int, input("Ingrese la fila y columna para colocar una pieza (0-4): ").split())
                # Solicita al jugador la nueva fila y columna para colocar su pieza
                movement = input("Ingrese el movimiento a realizar ('left', 'right', 'up' o 'down'): ")
                while movement not in ["left", "right", "up", "down"]:
                    movement = input("Ingrese un movimiento valido: ")
                if self.make_move(row, col, movement):  # Intenta realizar el movimiento
                    winner = self.check_winner()  # Verifica si hay un ganador
                    if winner:
                        self.print_board()
                        print(f"¡El jugador {winner} gana!")
                        break
                    self.switch_player()  # Cambia al siguiente jugador
                else:
                    print("Movimiento inválido, inténtelo de nuevo.")

# Inicia el juego
if __name__ == "__main__":
    game = Quixo() 
    game.play()


#Implemente negamax para que se jugara contra la computadora
#Hay un problema en la actualizaciónn del tablero ya que la compuadora no hace más de un movimiento
#Implemete un pequeño menu para controlar si se quiere jugar contra 1 o contra cpu
#Agregue un método que revisa si un movimiento es en esquina.
