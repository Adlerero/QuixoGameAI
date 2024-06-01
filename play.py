import time
from quixo import Quixo

def play():
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
        game.side = player
        

    turn = input("¿Cuál jugador va primero? Escoge 'O' o 'X'")
    while turn != 'O' and turn != 'X':
        turn = input("¿Cuál jugador va primero? Escoge 'O' o 'X'")
    
    game.current_player = turn
            

    # Bucle que controla el flujo del juego
    while True:
        game.print_board()  # Imprime el estado actual del tablero
        print(f"Turno del jugador {game.current_player}")
        if game.current_player == 'X':
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
                if game.make_move(row, col, movement, game.current_player):  # Intenta realizar el movimiento
                    winner = game.check_winner()  # Verifica si hay un ganador
                    if winner:
                        game.print_board()
                        print(f"¡El jugador {winner} gana!")
                        break
                    game.switch_player()  # Cambia al siguiente jugador
                else:
                    print("Movimiento inválido, inténtelo de nuevo.")
            else:  # Modo 1vCPU
                if game.side == 'X':
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
                    if game.make_move(row, col, movement, game.current_player):  # Intenta realizar el movimiento
                        winner = game.check_winner()  # Verifica si hay un ganador
                        if winner:
                            game.print_board()
                            print(f"¡El jugador {winner} gana!")
                            break
                        game.switch_player()  # Cambia al siguiente jugador
                    else:
                        print("Movimiento inválido, inténtelo de nuevo.")
                else:
                    print("Turno de la computadora")
                    start_time = time.time()
                    best_move = game.find_best_move()
                    if best_move:
                        row, col, movement, player = best_move
                        if game.make_move(row, col, movement, player):
                            winner = game.check_winner()
                            if winner:
                                game.print_board()
                                print(f"¡El jugador {winner} gana!")
                                break
                            print(f"La computadora ha hecho su movimiento en la casilla ({best_move[0]}, {best_move[1]}) hacia {best_move[2]}")
                        game.switch_player()
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
                if game.make_move(row, col, movement, game.current_player):  # Intenta realizar el movimiento
                    winner = game.check_winner()  # Verifica si hay un ganador
                    if winner:
                        game.print_board()
                        print(f"¡El jugador {winner} gana!")
                        break
                    game.switch_player()  # Cambia al siguiente jugador
                else:
                    print("Movimiento inválido, inténtelo de nuevo.")
            else:
                if game.side == 'O':
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
                    if game.make_move(row, col, movement, game.current_player):  # Intenta realizar el movimiento
                        winner = game.check_winner()  # Verifica si hay un ganador
                        if winner:
                            game.print_board()
                            print(f"¡El jugador {winner} gana!")
                            break
                        game.switch_player()  # Cambia al siguiente jugador
                    else:
                        print("Movimiento inválido, inténtelo de nuevo.")
                else:
                    print("Turno de la computadora")
                    start_time = time.time()
                    best_move = game.find_best_move()
                    if best_move:
                        row, col, movement, player = best_move
                        if game.make_move(row, col, movement, player):
                            winner = game.check_winner()
                            if winner:
                                game.print_board()
                                print(f"¡El jugador {winner} gana!")
                                break
                            print(f"La computadora ha hecho su movimiento en la casilla ({best_move[0]}, {best_move[1]}) hacia {best_move[2]}")
                        game.switch_player()
                    else:
                        print("La computadora no puede realizar ningún movimiento. ¡El juego termina en empate!")
                        break
                    end_time = time.time()
                    print(end_time - start_time)

# Inicia el juego
if __name__ == "__main__":
    game = Quixo() 
    play()