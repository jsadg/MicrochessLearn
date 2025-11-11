class MicroChess:
    def __init__(self):
        self.board = [
            ["k", "n", "b", "r"],
            ["p", None, None, None],
            [None, None, None, None],
            [None, None, None, "P"],
            ["R", "B", "N", "K"],
        ]
        
        self.white_to_move = True
        self.checkmate = False
        self.stalemate = False
        self.is_capture = False
        self.is_check = False
        self.white_castle = True
        self.black_castle = True

    def get_piece(self, row, col):
        return self.board[row][col]
    
    # Definitely rewrite in c engine manner 
    def is_square_attacked(self, row, col, byColor):
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                piece = self.board[r][c]
                if piece and self.get_piece_color(r,c) == byColor:
                    if self.check_piece_logic(r, c, row, col):
                        return True
        return False

    def generate_legal_moves(self):
        pass

    # Break up into standard piece movegen
    def check_piece_logic(self, row, col, newRow, newCol):
        if self.board[row][col] is not None:
            piece_type = self.board[row][col].upper()
            legal = True
            if(self.capture_same_color(row, col, newRow, newCol)):
                return False
            match piece_type:
                # Pawns
                case "P":
                    if self.get_piece_color(row, col) == "b":
                        normal_move = (newRow == row + 1 and col == newCol and self.get_piece(newRow, col) is None)
                        capture = (abs(newCol - col) == 1 and newRow - row == 1 and self.get_piece(newRow, newCol) is not None)
                        if not (normal_move or capture):
                            legal = False
                    elif self.get_piece_color(row, col) == "w":
                        normal_move = (newRow == row - 1 and col == newCol and self.get_piece(newRow, col) is None)
                        capture = (abs(newCol - col) == 1 and newRow - row == -1 and self.get_piece(newRow, newCol) is not None)
                        if not (normal_move or capture):
                            legal = False
                # Kings
                case "K":
                    if (abs(newRow - row), abs(newCol - col)) not in [(0, 1), (1, 0), (1, 1)]:
                        if self.get_piece_color(row, col) == "w" and row == 4 and col == 3:
                            if (newRow, newCol) == (4, 1):
                                if (self.white_castle and self.board[4][2] is None and self.board[4][1] is None and not self.is_square_attacked(4, 2, "b") and not self.is_square_attacked(4, 1, "b")):
                                    return True
                                else:
                                    return False
                        elif self.get_piece_color(row, col) == "b" and row == 0 and col == 0:
                            if (newRow, newCol) == (0, 2):
                                if (self.black_castle and self.board[0][2] is None and self.board[0][1] is None and not self.is_square_attacked(0, 2, "w") and not self.is_square_attacked(0, 1, "w")):
                                    return True
                                else:
                                    return False
                        return False
                # Queens
                case "Q":
                    if abs(newRow-row) == abs(newCol-col):
                        if newRow > row:
                            rowStep=1
                        else:
                            rowStep=-1
                        if newCol > col:
                            colStep=1
                        else:
                            colStep=-1
                        r = row+rowStep
                        c = col+colStep
                        while r != newRow and c != newCol:
                            if self.get_piece(r, c) is not None:
                                legal = False
                                break
                            r += rowStep
                            c += colStep
                    elif (newRow != row and newCol == col):
                        for i in range(min(row, newRow)+1, max(row, newRow)):
                            if self.get_piece(i, col) is not None:
                                legal = False
                                break
                    elif(newRow == row and newCol != col):
                        for i in range(min(col, newCol)+1, max(col, newCol)):
                            if self.get_piece(row,i) is not None:
                                legal = False   
                                break
                    else:
                        legal = False
                # Knights
                case "N":
                    if not (abs(newRow - row), abs(newCol - col)) in [(2, 1), (1, 2)]:
                        legal = False
                # Bishops
                case "B":
                    if abs(newRow-row) != abs(newCol-col):
                        legal=False
                    else:
                        if newRow > row:
                            rowStep=1
                        else:
                            rowStep=-1
                        if newCol > col:
                            colStep=1
                        else:
                            colStep=-1
                        r = row+rowStep
                        c = col+colStep
                        while r != newRow and c != newCol:
                            if self.get_piece(r, c) is not None:
                                legal = False
                                break
                            r += rowStep
                            c += colStep 
                # Rooks     
                case "R":
                    if newRow != row and newCol != col:
                        legal = False
                    elif (newRow != row and newCol == col):
                        for i in range(min(row, newRow)+1, max(row, newRow)):
                            if self.get_piece(i, col) is not None:
                                legal = False
                                break
                    elif(newRow == row and newCol != col):
                        for i in range(min(col, newCol)+1, max(col, newCol)):
                            if self.get_piece(row,i) is not None:
                                legal = False   
                                break                    
            return legal           
        return False
    
    def capture_same_color(self, row, col, newRow, newCol):
        return self.get_piece_color(newRow, newCol) is not None and (self.get_piece_color(newRow, newCol) == self.get_piece_color(row,col))
    
    def get_piece_color(self, row, col):
        if self.board[row][col] is None:
            return None
        if self.board[row][col].isupper():
            return "w"
        else:
            return "b"
        
    def make_move(self, row, col, newRow, newCol, promotion_choice=None):
        piece = self.get_piece(row, col)
        self.board[newRow][newCol] = self.board[row][col]
        self.board[row][col] = None
        # Move rook opposite of king for castling move
        if piece == "K" or piece == "k":
            if (row, col) == (4, 3) and (newRow, newCol) == (4, 1):
                self.board[4][2] = self.board[4][0]
                self.board[4][0] = None
            elif (row, col) == (0, 0) and (newRow, newCol) == (0, 2):
                self.board[0][1] = self.board[0][3]
                self.board[0][3] = None
                
        # Castle rights updaters
        if piece == "K":
            self.white_castle = False
        elif piece == "k":
            self.black_castle = False
        elif piece == "R":
            self.white_castle = False
        elif piece == "r":
            self.black_castle = False
            
        if (newRow, newCol) == (4,0):
            self.white_castle = False
        elif (newRow, newCol) == (0,3):
            self.black_castle = False

        # Pawn promotion
        if piece == "P" and newRow == 0:
            self.board[newRow][newCol] = promotion_choice.upper()
        elif piece == "p" and newRow == 4:
            self.board[newRow][newCol] = promotion_choice.lower()

        #Flip side at end of move
        self.white_to_move = not self.white_to_move