#Adler Antonio Calvillo Arellano
#Jared López García

class Quixo:
    def __init__(self):
        # Inicializa un tablero de 5x5 lleno de espacios vacíos y establece el jugador actual en 'X'
        self.board = [[' ' for _ in range(5)] for _ in range(5)]
        self.current_player = 'X'

    def print_board(self):
        # Imprime el tablero en su estado actual
        for row in self.board:
            print('  |  '.join(row))  # Imprime una fila del tablero con separadores '|'
            print('---' * 9)  # Imprime una línea divisoria entre filas

    def is_valid_move(self, row, col):
        # Verifica si un movimiento es válido (la pieza debe estar en el borde y ser vacía o del jugador actual)
        if row == 0 or row == 4 or col == 0 or col == 4:
            if self.board[row][col] == ' ' or self.board[row][col] == self.current_player:
                return True  # Movimiento válido
        return False  # Movimiento inválido

    def make_move(self, row, col, movement):
        # Verifica el lugar desde el que se toma la pieza es válido
        if self.is_valid_move(row, col):
            #Movimientos no validos en aristas
            if col != 0 or col != 4:
                if row == 0 and movement == "up":
                    print("Asegúrese de colocar la pieza en un lugar diferente al que la tomó.")
                    return False
                if row == 4 and movement == "down":
                    print("Asegúrese de colocar la pieza en un lugar diferente al que la tomó.")
                    return False
            if row != 0 or row != 4:
                if col == 0 and movement == "left":
                    print("Asegúrese de colocar la pieza en un lugar diferente al que la tomó.")
                    return False
                if col == 4 and movement == "right":
                    print("Asegúrese de colocar la pieza en un lugar diferente al que la tomó.")
                    return False
            #Movimientos no validos en esquinas 
            if row == 0 and col == 0 and movement == "up":
                print("Asegúrese de colocar la pieza en un lugar diferente al que la tomó.")
                return False
            if row == 0 and col == 0 and movement == "left":
                print("Asegúrese de colocar la pieza en un lugar diferente al que la tomó.")
                return False
            if row == 0 and col == 4 and movement == "up":
                print("Asegúrese de colocar la pieza en un lugar diferente al que la tomó.")
                return False
            if row == 0 and col == 4 and movement == "right":
                print("Asegúrese de colocar la pieza en un lugar diferente al que la tomó.")
                return False
            if row == 4 and col == 0 and movement == "down":
                print("Asegúrese de colocar la pieza en un lugar diferente al que la tomó.")
                return False
            if row == 4 and col == 0 and movement == "left":
                print("Asegúrese de colocar la pieza en un lugar diferente al que la tomó.")
                return False
            if row == 4 and col == 4 and movement == "down":
                print("Asegúrese de colocar la pieza en un lugar diferente al que la tomó.")
                return False
            if row == 4 and col == 4 and movement == "right":
                print("Asegúrese de colocar la pieza en un lugar diferente al que la tomó.")
                return False

            #Movimiento valido
            else:
                # Establece la pieza en la nueva posición
                self.board[row][col] = self.current_player
            # Movimiento horizontal
                if movement == "right":  # Desplazamiento a la derecha
                    for i in range(col, 4):
                        self.board[row][i] = self.board[row][i + 1]  # Desplaza las piezas hacia la izquierda
                    self.board[row][4] = self.current_player  # Coloca la pieza en la nueva posición
                if movement == "left":  # Desplazamiento a la izquierda
                    for i in range(col, 0, -1):
                        self.board[row][i] = self.board[row][i - 1]  # Desplaza las piezas hacia la derecha
                    self.board[row][0] = self.current_player  # Coloca la pieza en la nueva posición
            # Movimiento vertical
                if movement == "down":  # Desplazamiento hacia abajo
                    for i in range(row, 4):
                        self.board[i][col] = self.board[i + 1][col]  # Desplaza las piezas hacia arriba
                    self.board[4][col] = self.current_player  # Coloca la pieza en la nueva posición
                if movement == "up":  # Desplazamiento hacia arriba
                    for i in range(row, 0, -1):
                        self.board[i][col] = self.board[i - 1][col]  # Desplaza las piezas hacia abajo
                    self.board[0][col] = self.current_player  # Coloca la pieza en la nueva posición
                return True  # Movimiento realizado con éxito
        print("Asegúrese de tomar una pieza que esté en los bordes.")
        return False  # Movimiento inválido

    def check_winner(self):
        # Comprueba si hay un ganador
        lines = []
        # Añade todas las filas al conjunto de líneas a verificar
        for row in self.board:
            lines.append(row)
        # Añade todas las columnas al conjunto de líneas a verificar
        for col in range(5):
            lines.append([self.board[row][col] for row in range(5)])
        # Añade las diagonales al conjunto de líneas a verificar
        lines.append([self.board[i][i] for i in range(5)])
        lines.append([self.board[i][4-i] for i in range(5)])

        # Comprueba cada línea para ver si hay un ganador
        # En caso de formarse 5 en fila de los dos bandos en una jugada, gana el que hizo la jugada.
        # por ello se revisa primero al current player.
        if self.current_player == 'X':
            for line in lines:
                if all(cell == 'X' for cell in line):
                    return 'X'  # El jugador X ha ganado
            for line in lines:
                if all(cell == 'O' for cell in line):
                    return 'O'  # El jugador O ha ganado
        else:
            for line in lines:
                if all(cell == 'O' for cell in line):
                    return 'O'  # El jugador X ha ganado
            for line in lines:
                if all(cell == 'X' for cell in line):
                    return 'X'  # El jugador O ha ganado
        return None  # No hay ganador aún

    def switch_player(self):
        # Cambia el turno al otro jugador
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def play(self):
        # Controla el flujo del juego
        while True:
            self.print_board()  # Imprime el tablero actual
            print(f"Turno del jugador {self.current_player}")
            # Solicita al jugador que ingrese la fila y columna de la pieza a mover
            row, col = map(int, input("Ingrese la fila y columna para recoger una pieza (0-4): ").split())
            # Solicita al jugador que ingrese la nueva fila y columna para colocar la pieza
            movement = input("Ingrese el movimiento a realizar('left', 'right', 'up' o 'down'): ")
            while movement != "left" and movement != "right" and movement != "up" and movement != "down":
                movement = input("Ingrese un movimiento valido: ")
            if self.make_move(row, col, movement):  # Intenta realizar el movimiento
                winner = self.check_winner()  # Verifica si hay un ganador
                if winner:
                    self.print_board()  # Imprime el tablero final
                    print(f"¡El jugador {winner} gana!")  # Anuncia al ganador
                    break  # Termina el juego
                self.switch_player()  # Cambia de jugador
            else:
                print("Movimiento inválido, inténtelo de nuevo.")

# Código principal para iniciar el juego
if __name__ == "__main__":
    game = Quixo()  # Crea una instancia del juego Quixo
    game.play()  # Inicia el juego


"""
Anotaciones:
-Implementé movimientos con sus respectivas limitaciones. Solo se puede tomar de los bordes, y si intentas
poner una pieza en el lugar que la tomaste, no puedes hacerlo.
-Implementé sistema de ganador y perdedor, así como cambio de turno cambiando self.current_player.
-Implementé tablero en el constructor self.board y sistema para jugar implementado en play.
-Corregi empate. En caso de 2 5 en raya a la vez generados en una jugada, gana el jugador que hizo la jugada.
"""