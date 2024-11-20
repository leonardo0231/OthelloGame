import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QWidget, QStackedWidget, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QRect
from PyQt5.QtGui import QColor


class AlphaBeta:

    def __init__(self, root_node):
            self.root = root_node
            return
    
    def alpha_beta_search(self, node):
        infinity = float('inf')
        best_val = -infinity
        beta = infinity
        successors = self.getSuccessors(node)
        best_state = None

        for state in successors:
            value = self.min_value(state, best_val, beta)
            if value > best_val:
                best_val = value
                best_state = state
        
        return best_state

    def max_value(self, node, alpha, beta):
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = -infinity
        successors = self.getSuccessors(node)

        for state in successors:
            value = max(value, self.min_value(state, alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value
    

    def min_value(self, node, alpha, beta):
        if self.isTerminal(node):
            return self.getUtility(node)
        infinity = float('inf')
        value = infinity
        successors = self.getSuccessors(node)

        for state in successors:
            value = min(value, self.max_value(state, alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value
    

    def getSuccessors(self, node):
        assert node is not None
        return node.children

    def isTerminal(self, node):
        assert node is not None
        return len(node.children) == 0
 
    def getUtility(self, node):
        assert node is not None
        return node.value


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Othello Game - Select Mode")
        self.setGeometry(500, 200, 400, 300) 
        self.central_widget = QStackedWidget()  
        self.setCentralWidget(self.central_widget)
        
        self.selected_mode = None

        self.initUI()

    def initUI(self):
        mode_selection_widget = QWidget()
        mode_layout = QVBoxLayout()
        
        mode_label = QLabel("Select Game Mode:")
        mode_label.setAlignment(Qt.AlignCenter)
        mode_layout.addWidget(mode_label)
        
        pvp_button = QPushButton("Player vs Player")
        pva_button = QPushButton("Player vs AI")
        # pvp_button.clicked.connect(self.show_board_size_selection)
        # pva_button.clicked.connect(self.show_board_size_selection_pva)
        pvp_button.clicked.connect(lambda: self.select_mode("Player vs Player"))
        pva_button.clicked.connect(lambda: self.select_mode("Player vs AI"))
        mode_layout.addWidget(pvp_button)
        mode_layout.addWidget(pva_button)
        
        mode_selection_widget.setLayout(mode_layout)
        self.central_widget.addWidget(mode_selection_widget)

        self.board_size_widget = QWidget()
        board_size_layout = QVBoxLayout()
        
        size_label = QLabel("Select Board Size:")
        size_label.setAlignment(Qt.AlignCenter)
        board_size_layout.addWidget(size_label)
        
        self.size_combo_box = QComboBox()
        self.size_combo_box.addItems(["6", "8", "10", "12"])
        board_size_layout.addWidget(self.size_combo_box)
        
        start_button = QPushButton("Start Game")
        start_button.clicked.connect(self.start_game)
        board_size_layout.addWidget(start_button)
        
        self.board_size_widget.setLayout(board_size_layout)
        self.central_widget.addWidget(self.board_size_widget)

    def select_mode(self, mode):
        self.selected_mode = mode
        self.show_board_size_selection()

    def show_board_size_selection(self):
        self.central_widget.setCurrentWidget(self.board_size_widget)

    def start_game(self):
        board_size = int(self.size_combo_box.currentText())
        self.othello_game = OthelloGame(board_size, self.selected_mode)
        self.othello_game.show()
        self.close()

class GameNode:
    def __init__(self, board, current_player, move=None, value=None):
        self.board = board
        self.current_player = current_player
        self.move = move
        self.children = []
        self.value = value


class OthelloGame(QMainWindow):
    def __init__(self, board_size, mode="Player vs Player"):
        super().__init__()
        self.board_size = board_size
        self.mode = mode
        self.setWindowTitle("Othello Game")
        self.setGeometry(300, 100, 600, 600)
        
        self.current_player = 'black'
        self.black_score = 2
        self.white_score = 2
        self.board = [[None for _ in range(board_size)] for _ in range(board_size)]
        
        self.init_game_ui()
        self.initialize_board()

    def init_game_ui(self):
        main_layout = QVBoxLayout()
        
        self.mode_layout = QHBoxLayout()
        self.mode_label = QLabel(f"game mode: {str(self.mode)}")
        self.mode_layout.addWidget(self.mode_label)

        score_layout = QHBoxLayout()
        self.turn_label = QLabel(f"Turn: {self.current_player.capitalize()}")
        self.black_score_label = QLabel(f"Black: {self.black_score}")
        self.white_score_label = QLabel(f"White: {self.white_score}")
        
        score_layout.addWidget(self.turn_label)
        score_layout.addWidget(self.black_score_label)
        score_layout.addWidget(self.white_score_label)
        
        main_layout.addLayout(score_layout)
        main_layout.addLayout(self.mode_layout)
        
        board_widget = QWidget()
        self.grid_layout = QGridLayout(board_widget)
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                cell = QPushButton("")
                cell.setFixedSize(50, 50)
                cell.setStyleSheet("background-color: grey; border: 1px solid black;")
                cell.clicked.connect(lambda _, r=row, c=col: self.handle_move(r, c))
                self.grid_layout.addWidget(cell, row, col)
                self.board[row][col] = cell

        main_layout.addWidget(board_widget)
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def initialize_board(self):
        mid = self.board_size // 2
        self.place_piece(mid - 1, mid - 1, 'white')
        self.place_piece(mid - 1, mid, 'black')
        self.place_piece(mid, mid - 1, 'black')
        self.place_piece(mid, mid, 'white')

    def place_piece(self, row, col, color):
        button = self.board[row][col]
        button.setStyleSheet(f"background-color: {color}; border-radius: 25px;")
        button.setProperty("color", color)
        anim = QPropertyAnimation(button, b"geometry")
        anim.setDuration(200)
        anim.setStartValue(QRect(button.x(), button.y(), 10, 10))
        anim.setEndValue(QRect(button.x(), button.y(), 50, 50))
        anim.start()

    def handle_move(self, row, col):
        if self.is_legal_move(row, col, self.current_player):
            self.place_piece(row, col, self.current_player)
            self.flip_pieces(row, col)
            self.update_scores()
            self.update_turn_display()

            self.current_player = 'white' if self.current_player == 'black' else 'black'

        if not self.has_legal_move(self.current_player) and not self.has_legal_move(self.opponent(self.current_player)):
            self.end_game()
            return
        
        if not self.has_legal_move(self.current_player):
            self.current_player = 'white' if self.current_player == 'black' else 'black'
            self.update_turn_display()

        if  self.mode == "Player vs AI" and self.current_player == "white":
            self.ai_move()

    def ai_move(self):
        root_node = self.create_game_tree(self.board, 'white')
        alpha_beta = AlphaBeta(root_node)
        best_state = alpha_beta.alpha_beta_search(root_node)
        if best_state and best_state.move:
            row, col = best_state.move
            self.place_piece(row, col, 'white')
            self.flip_pieces(row, col)
            self.update_scores()
            self.update_turn_display()
            self.current_player = 'black'

    def has_legal_move(self, player):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.is_legal_move(row, col, player):
                    return True
        return False
    
    def is_legal_move(self, row, col, player):
        if self.board[row][col].property("color") is not None:
            return False
        
        opponent = 'white' if player == 'black' else 'black'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            found_opponent = False
            
            while 0 <= r < self.board_size and 0 <= c < self.board_size:
                if self.board[r][c].property("color") == opponent:
                    found_opponent = True
                elif self.board[r][c].property("color") == player and found_opponent:
                    return True
                else:
                    break
                
                r += dr
                c += dc
                
        return False

    def flip_pieces(self, row, col):
        opponent = 'white' if self.current_player == 'black' else 'black'
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            pieces_to_flip = []
            
            while 0 <= r < self.board_size and 0 <= c < self.board_size:
                if self.board[r][c].property("color") == opponent:
                    pieces_to_flip.append((r, c))
                elif self.board[r][c].property("color") == self.current_player:
                    for flip_r, flip_c in pieces_to_flip:
                        self.place_piece(flip_r, flip_c, self.current_player)
                    break
                else:
                    break
                
                r += dr
                c += dc

    def update_scores(self):
        self.black_score = sum(button.property("color") == "black" for row in self.board for button in row)
        self.white_score = sum(button.property("color") == "white" for row in self.board for button in row)
        self.black_score_label.setText(f"Black: {self.black_score}")
        self.white_score_label.setText(f"White: {self.white_score}")

    def update_turn_display(self):
        self.turn_label.setText(f"Turn: {self.current_player.capitalize()}")
    
    def opponent(self, player):
        return 'white' if player == 'black' else 'black'
    
    def create_game_tree(self, board, player, depth=3):
        if depth == 0 or self.is_terminal_state(board):
            utility = self.evaluate_board(board, player)
            return GameNode(board, player, value=utility)
        
        root = GameNode(board, player)
        legal_moves = [(r,c) for r in range(self.board_size) for c in range(self.board_size)
                        if self.is_legal_move(r, c, player)]
        
        for move in legal_moves:
            new_board = self.simulate_move(board, move, player)
            child_node = self.create_game_tree(new_board, 'black' if player == 'white' else 'white', depth -1)
            child_node.move = move
            root.children.append(child_node)

        return root

    def evaluate_board (self, board, player):
        player_score = sum(row.count(player) for row in board)
        opponent = 'black' if player == 'white' else 'white'
        opponent_score = sum(row.count(opponent) for row in board)
        return player_score - opponent_score

    def simulate_move (self, board, move, player):
        new_board = [row[:] for row in board]
        row, col = move
        new_board[row][col] = player

        return new_board

    def end_game(self):
        winner = "Black" if self.black_score > self.white_score else "White" if self.white_score > self.black_score else "Tie"
        # msg = f"Game Over! Winner: {winner}" if winner != "Tie" else "Game Over! It's a tie!"
        msg = QMessageBox()
        msg.setWindowTitle("Game over thanks for playing whit me")
        if winner == "Tie":
            msg.setText("Game over! It's tie!")
        else:
            msg.setText(f"Game over! the winner is {winner}")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def is_terminal_state(self, board):
        return not any(self.is_legal_move(r, c, 'white') or self.is_legal_move(r, c, 'black')
                   for r in range(self.board_size) for c in range(self.board_size))
    

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = StartWindow()
    window.show()
    sys.exit(app.exec_())
