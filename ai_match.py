from quixo import Quixo
import random
import time

class AIMatch:
    def __init__(self, quixo):
        self.quixo = quixo

    def random_vs_heuristic1(self):
        random_number = random.randint(0, 1)
        if random_number == 0:
            self.quixo.current_player = 'X'
        else:
            self.quixo.current_player = 'O'
        while True:
            self.quixo.print_board()
            if self.quixo.current_player == 'X':
                print("Turno del random")
                start_time = time.time()
                possible_moves = self.quixo.get_possible_moves()
                random_move = random.choice(possible_moves)
                if random_move:
                    row, col, movement = random_move
                    if self.quixo.make_move(row, col, movement, self.quixo.current_player):
                        winner = self.quixo.check_winner()
                        if winner:
                            self.quixo.print_board()
                            print(f"¡El jugador {winner} gana!")
                            break
                        print(f"Random ha hecho su movimiento en la casilla ({random_move[0]}, {random_move[1]}) hacia {random_move[2]}")
                    self.quixo.switch_player()
                else:
                    print("Random no puede realizar ningún movimiento. ¡El juego termina en empate!")
                    break
                end_time = time.time()
                print(end_time - start_time)
            else:
                print("Turno de la computadora")
                start_time = time.time()
                best_move = self.quixo.find_best_move()
                if best_move:
                    row, col, movement, player = best_move
                    if self.quixo.make_move(row, col, movement, player):
                        winner = self.quixo.check_winner()
                        if winner:
                            self.quixo.print_board()
                            print(f"¡El jugador {winner} gana!")
                            break
                        print(f"La computadora ha hecho su movimiento en la casilla ({best_move[0]}, {best_move[1]}) hacia {best_move[2]}")
                    self.quixo.switch_player()
                else:
                    print("La computadora no puede realizar ningún movimiento. ¡El juego termina en empate!")
                    break
                end_time = time.time()
                print(end_time - start_time)
        

game = Quixo()
ai = AIMatch(game)
ai.random_vs_heuristic1()