import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import Qt


""""
                                                ### MiniMax ###
"""
class MiniMax:
    """
    print utility value of root node (assuming it is max)
    print names of all nodes visited during search
    """
    def __init__(self, game_tree):
        self.game_tree = game_tree
        self.root = game_tree.root
        self.currentNode = None
        self.successors = []
        return
    
    def minimax(self, node):
        # first, find max value
        best_val = self.max_value(node)

        """
        second, find the node which HAS that max value
        -> means we need to propagate the values back up the tree as part of our minimax algorithm 
        """
        successors = self.getSuccessors(node)
        print(f"MiniMax: Utility Value of Root Node: = {str(best_val)}")

        best_move = None
        for elem in successors:     # —> Need to propagate values up tree for this to work
            if elem.value == best_val:
                best_move = elem
                break

        return best_move
    
    def max_value(self, node):
        print(f"MiniMax -> MAX: Visited Node :: {node.Name}")
        if self.isTerminal(node):
            return self.getUtility(node)
        
        infinity = float('inf')
        max_value = -infinity
        successor_state = self.getSuccessors(node)

        for state in successor_state:
            max_value = max(max_value, self.min_value(state))
        return max_value
    
    def min_value(self, node):
        print(f"MiniMax -> MIN: Visited node :: {node.name}")
        if self.isTerminal(node):
            return self.getUtility(node)
        
        infinity = float('inf')
        min_value = infinity
        successor_state = self.getSuccessors(node)
        for state in successor_state:
            min_value = min(min_value, self.max_value(state))
        return min_value
    

    # successor states in a game tree are the child nodes…
    def getSuccessors(self, node):
        assert node is not None
        return node.children
    
    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
    def isTerminal(self, node):
        assert node is not None
        return len(node.children) == 0
    

    def getUtility(self, node):
        assert node is not None
        return node.value


""""
                                                ### MiniMax A-B ###
"""
class AlphaBeta:

    def __init__(self, game_tree):
            self.game_tree = game_tree
            self.root = game_tree.root
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
        
        print(f"AlphaBeta: Utility Value of Root Node: = {str(best_val)}")
        print(f"AlphaBeta: Best State is: {str(best_state.Name)}")
        return best_state
    def max_value(self, node, alpha, beta):
        print(f"AlphaBeta->MAX: Visited Node :: {node.Name}")
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
        print(f"AlphaBeta->MIX: Visited Node :: {node.Name}")
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

class OthelloGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Othello Game")
        self.setGeometry(100, 100, 400, 440)
        
        self.current_player = "black"
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.grid_layout = QGridLayout(self.central_widget)
        self.create_board()

    def create_board(self, rows=8, cols=8):
        self.cells = {}

        for row in range(rows):
            for col in range(cols):

                cell = QPushButton(self)
                cell.setFixedSize(50, 50)
                cell.setStyleSheet("background-color: gray;")

                cell.clicked.connect(lambda _, r=row, c=col: self.cell_clicked(r, c))

                self.grid_layout.addWidget(cell, row, col)
                self.cells[(row, col)] = cell


        self.initialize_othello_pieces()

    def initialize_othello_pieces(self):
        initial_positions = [(3,3, "white"), (3,4, "black"), (4,4, "white"), (4,3, "black")]
        for row, col, color in initial_positions:
            self.set_price(row, col, color)

    def set_price(self, row, col, color):
        cell = self.cells[(row, col)]
        cell.setStyleSheet(f"background-color: {color}; border_radius: 25ps;")

    def cell_clicked(self, row, col):
        if self.is_valid_move(row, col, self.current_player):
            self.set_price(row, col, self.current_player)
            self.flip_pieces(row, col, self.current_player)
            self.current_player = "white" if self.current_player == "black" else "black"
    
    def is_valid_move(self, row, col, player_color):
        if self.cells[(row, col)].styleSheet() != "background-color: gray;":
            return False
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        valid = False
        for dx, dy in directions:
            if self.check_direction(row, col, dx, dy, player_color):
                valid = True
        return valid
    
    def check_direction(self, row, col, dx, dy, player_color):
        opponent_color = "white" if player_color == "black" else "black"
        r, c = row + dx, col + dy
        pieces_to_flip = []

        while (r,c) in self.cells and self.cells[(r,c)].styleSheet() == f"background-color: {opponent_color};":
            pieces_to_flip.append((r,c))
            r += dx
            c += dy
        
        if (r,c) in self.cells and self.cells[(r,c)].styleSheet() == f"background-color: {player_color};":
            return pieces_to_flip
        
        return []
    
    def flip_pieces(self, row, col, player_color):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]
        for dx, dy in directions:
            pieces_to_flip = self.check_direction(row, col, dx, dy, player_color)
            for r,c in pieces_to_flip:
                self.set_price(r,c, player_color)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OthelloGame()
    window.show()
    sys.exit(app.exec_())
