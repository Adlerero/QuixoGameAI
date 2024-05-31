def evaluate_board(self):
        def evaluate_line(line, player, opponent):
            if player in line and opponent not in line:
                return line.count(player)  # Más puntos por más piezas sin oponente en la línea
            elif opponent in line and player not in line:
                return -line.count(opponent)  # Penaliza si el oponente tiene piezas sin que estés tú
            return 0

        def center_control(board, player, opponent):
            center_value = 3  # Valor ajustable para la importancia del centro
            center_positions = [(1,1), (1,3), (2,2), (3,1), (3,3)]  # Posiciones que rodean el centro real
            score = 0
            # Verificar si el jugador controla el centro real
            if board[2][2] == player:
                score += center_value * 2  # Doble puntuación para el centro exacto
            elif board[2][2] == opponent:
                score -= center_value * 2
            # Verificar las posiciones alrededor del centro
            for pos in center_positions:
                if board[pos[0]][pos[1]] == player:
                    score += center_value
                elif board[pos[0]][pos[1]] == opponent:
                    score -= center_value
            return score

        score = 0
        # Evalúa filas y columnas
        for i in range(5):
            row = self.board[i]
            column = [self.board[j][i] for j in range(5)]
            
            # Suma puntos si 'X' está cerca de completar una línea
            score += evaluate_line(row, 'X', 'O')
            score += evaluate_line(column, 'X', 'O')
            
            # Resta puntos si 'O' está cerca de completar una línea
            score -= evaluate_line(row, 'O', 'X')
            score -= evaluate_line(column, 'O', 'X')
        
        # Evalúa diagonales
        diag1 = [self.board[i][i] for i in range(5)]
        diag2 = [self.board[i][4-i] for i in range(5)]
        score += evaluate_line(diag1, 'X', 'O')
        score += evaluate_line(diag2, 'X', 'O')
        score -= evaluate_line(diag1, 'O', 'X')
        score -= evaluate_line(diag2, 'O', 'X')
        
        # Puntos adicionales por control del centro
        score += center_control(self.board, 'X', 'O')
        score -= center_control(self.board, 'O', 'X')

        return score







def evaluate_board(board):
    score = 0
    # Evalúa filas y columnas
    for i in range(5):
        row = board[i]
        column = [board[j][i] for j in range(5)]
        
        # Suma puntos si 'X' está cerca de completar una línea
        score += evaluate_line(row, 'X', 'O')
        score += evaluate_line(column, 'X', 'O')
        
        # Resta puntos si 'O' está cerca de completar una línea
        score -= evaluate_line(row, 'O', 'X')
        score -= evaluate_line(column, 'O', 'X')
    
    # Evalúa diagonales
    diag1 = [board[i][i] for i in range(5)]
    diag2 = [board[i][4-i] for i in range(5)]
    score += evaluate_line(diag1, 'X', 'O')
    score += evaluate_line(diag2, 'X', 'O')
    score -= evaluate_line(diag1, 'O', 'X')
    score -= evaluate_line(diag2, 'O', 'X')

    return score

def evaluate_line(line, player, opponent):
    if player in line and opponent not in line:
        return line.count(player)
    elif opponent in line and player not in line:
        return -line.count(opponent)
    return 0

# Ejemplo de uso:
board = [
    ['X', 'X', ' ', 'O', ' '],
    ['X', 'O', 'O', ' ', ' '],
    [' ', 'X', ' ', ' ', ' '],
    [' ', ' ', 'O', ' ', ' '],
    ['X', ' ', ' ', ' ', 'O']
]

print("Heuristic score for X as maximizer:", evaluate_board(board))




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
        
        # Si el jugador ya ha ganado, devuelve un puntaje alto.
        if count_series(player, 5) > 0:
            return float('inf') if player == 'X' else float('-inf')

        X_score = (100 * count_series('X', 4) +
                10 * count_series('X', 3) + 1 * count_series('X', 2) + center_control('X'))

        O_score = (100 * count_series('O', 4) +
                10 * count_series('O', 3) + 1 * count_series('O', 2) + center_control('O'))

        if player == 'X':
            return X_score - O_score
        else:
            return O_score - X_score
        

def evaluate_board(self):
        def evaluate_line(line, player, opponent):
            if player in line and opponent not in line:
                return line.count(player)  # Más puntos por más piezas sin oponente en la línea
            elif opponent in line and player not in line:
                return -line.count(opponent)  # Penaliza si el oponente tiene piezas sin que estés tú
            return 0

        def center_control(board, player, opponent):
            center_value = 3  # Valor ajustable para la importancia del centro
            center_positions = [(1,1), (1,3), (3,1), (3,3)]  # Posiciones que rodean el centro real
            score = 0
            # Verificar si el jugador controla el centro real
            if board[2][2] == player:
                score += center_value * 2  # Doble puntuación para el centro exacto
            # Verificar las posiciones alrededor del centro
            for pos in center_positions:
                if board[pos[0]][pos[1]] == player:
                    score += center_value
            return score

        xscore = 0
        oscore = 0
        # Evalúa filas y columnas
        for i in range(5):
            row = self.board[i]
            column = [self.board[j][i] for j in range(5)]
            
            # Suma puntos si 'X' está cerca de completar una línea
            xscore += evaluate_line(row, 'X', 'O')
            xscore += evaluate_line(column, 'X', 'O')
            
            # Resta puntos si 'O' está cerca de completar una línea
            oscore += evaluate_line(row, 'O', 'X')
            oscore += evaluate_line(column, 'O', 'X')
        
        # Evalúa diagonales
        diag1 = [self.board[i][i] for i in range(5)]
        diag2 = [self.board[i][4-i] for i in range(5)]
        xscore += evaluate_line(diag1, 'X', 'O')
        xscore += evaluate_line(diag2, 'X', 'O')
        oscore += evaluate_line(diag1, 'O', 'X')
        oscore += evaluate_line(diag2, 'O', 'X')
        
        # Puntos adicionales por control del centro
        xscore += center_control(self.board, 'X', 'O')
        oscore += center_control(self.board, 'O', 'X')

        if self.current_player == 'X':
            return xscore - oscore
        else:
            return oscore - xscore
        











def evaluate_board(self, is_maximizing):
        def evaluate_line(line, player, opponent):
            if player in line and opponent not in line:
                return line.count(player)  # Más puntos por más piezas sin oponente en la línea
            elif opponent in line and player not in line:
                return -line.count(opponent)  # Penaliza si el oponente tiene piezas sin que estés tú
            return 0

        def center_control(board, player, opponent):
            center_value = 3  # Valor ajustable para la importancia del centro
            center_positions = [(1,1), (1,3), (3,1), (3,3)]  # Posiciones que rodean el centro real
            score = 0
            # Verificar si el jugador controla el centro real
            if board[2][2] == player:
                score += center_value * 2  # Doble puntuación para el centro exacto
            # Verificar las posiciones alrededor del centro
            for pos in center_positions:
                if board[pos[0]][pos[1]] == player:
                    score += center_value
            return score

        xscore = 0
        oscore = 0
        # Evalúa filas y columnas
        for i in range(5):
            row = self.board[i]
            column = [self.board[j][i] for j in range(5)]
            
            # Suma puntos si 'X' está cerca de completar una línea
            xscore += evaluate_line(row, 'X', 'O')
            xscore += evaluate_line(column, 'X', 'O')
            
            # Resta puntos si 'O' está cerca de completar una línea
            oscore += evaluate_line(row, 'O', 'X')
            oscore += evaluate_line(column, 'O', 'X')
        
        # Evalúa diagonales
        diag1 = [self.board[i][i] for i in range(5)]
        diag2 = [self.board[i][4-i] for i in range(5)]
        xscore += evaluate_line(diag1, 'X', 'O')
        xscore += evaluate_line(diag2, 'X', 'O')
        oscore += evaluate_line(diag1, 'O', 'X')
        oscore += evaluate_line(diag2, 'O', 'X')
        
        # Puntos adicionales por control del centro
        xscore += center_control(self.board, 'X', 'O')
        oscore += center_control(self.board, 'O', 'X')

        if is_maximizing:
            return xscore - oscore
        else:
            return oscore - xscore