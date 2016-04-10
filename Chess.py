__author__ = 'Maksymilian Mika'

import copy


class Piece:
    def __init__(self, piece_type, color, directions, slide):
        """
        Used to create piece of given type and color.
        :param piece_type: Type of given piece. Example: Rook
        :param color: Color of piece. Example: White
        :param directions: Directions the piece can travel.
        :param slide: If the piece can slide.
        """
        self.color = color
        self.piece_type = piece_type
        self.directions = directions
        self.slide = slide

    def __str__(self):
        """
        Neatly print information about the piece.
        :return: String describing the piece.
        """
        return self.color[0] + self.piece_type[0]


rook_directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
knight_directions = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
bishop_directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
queen_directions = rook_directions + bishop_directions
king_directions = queen_directions

white_pawn = Piece("Pawn", "White", None, False)  # Pawns are more complicated.
white_rook = Piece("Rook", "White", rook_directions, True)
white_knight = Piece("Knight", "White", knight_directions, False)
white_bishop = Piece("Bishop", "White", bishop_directions, True)
white_queen = Piece("Queen", "White", queen_directions, True)
white_king = Piece("King", "White", king_directions, False)

black_pawn = Piece("Pawn", "Black", None, False)  # Pawns are more complicated.
black_rook = Piece("Rook", "Black", rook_directions, True)
black_knight = Piece("Knight", "Black", knight_directions, False)
black_bishop = Piece("Bishop", "Black", bishop_directions, True)
black_queen = Piece("Queen", "Black", queen_directions, True)
black_king = Piece("King", "Black", king_directions, False)


def opposite_color(color):
    """
    Returns color opposite to given color. Example: Black -> White
    :param color: Color. Example: White
    :return: Opposite color.
    """
    if color == "White":
        return "Black"
    return "White"


def get_piece(piece_type, color):
    """
    Get piece object from it's parameters.
    :param piece_type: Desired pieces type. Example: Rook
    :param color: Desired pieces color. Example: White
    :return: Object with given parameters.
    """
    if color == "White":
        if piece_type == "Pawn":
            return white_pawn
        if piece_type == "Rook":
            return white_rook
        if piece_type == "Knight":
            return white_knight
        if piece_type == "Bishop":
            return white_bishop
        if piece_type == "Queen":
            return white_queen
        if piece_type == "King":
            return white_king
    else:
        if piece_type == "Pawn":
            return black_pawn
        if piece_type == "Rook":
            return black_rook
        if piece_type == "Knight":
            return black_knight
        if piece_type == "Bishop":
            return black_bishop
        if piece_type == "Queen":
            return black_queen
        if piece_type == "King":
            return black_king


def convert_index(index):
    """
    Converts index representation to point representation.
    :param index: Index in the table.
    :return: Point in two dimensions.
    """
    snd = index / 8
    return index - snd * 8, snd


def convert_point((x, y)):
    """
    Converts point in two dimensions to index in the tabke,
    :return: Index.
    """
    return x + y * 8


def check_bounds((x, y)):
    """
    Check if given point is in bounds of the board.
    :return:
    """
    return 0 <= x < 8 and 0 <= y < 8


def add_vectors((x, y), (dx, dy)):
    """
    Sum two vectors together.
    :return: Resulting vector.
    """
    return x + dx, y + dy


class Board:
    def __init__(self):
        """
        Initial setting of the board.
        """
        self.table = [white_rook, white_knight, white_bishop, white_queen, white_king, white_bishop, white_knight,
                      white_rook]
        for i in range(8):
            self.table.append(white_pawn)
        for i in range(4):
            for j in range(8):
                self.table.append(None)
        for i in range(8):
            self.table.append(black_pawn)
        self.table += [black_rook, black_knight, black_bishop, black_queen, black_king, black_bishop, black_knight,
                       black_rook]
        self.turn = "White"
        self.white_castle = (True, True)
        self.black_castle = (True, True)
        self.en_passant = -1

        self.moves = []
        for i in range(64):
            self.moves.append([])
        self.win = None

    def __str__(self):
        string = "  0  1  2  3  4  5  6  7 \n"
        for y in range(8):
            string += str(y) + " "
            for x in range(8):
                piece = self.table[convert_point((x, y))]
                if piece is None:
                    string += ".. "
                else:
                    string += piece.__str__() + " "
            string += "\n"
        return string

    def is_checked(self, point):
        """
        Check if given point is checked by the opposite color.
        :param point: Point to check.
        :return: True if the point is checked. False otherwise.
        """

        def check_direction(pieces, direction, slide):
            current = add_vectors(point, direction)
            while check_bounds(current):
                field = self.table[convert_point(current)]
                if field is not None:
                    return field.piece_type in pieces and field.color != self.turn
                if not slide:
                    break
                current = add_vectors(current, direction)
            return False

        def check_directions(pieces, directions, slide):
            for direction in directions:
                if check_direction(pieces, direction, slide):
                    return True
            return False

        if self.turn == "White":
            pawn_directions = [(-1, 1), (1, 1)]
        else:
            pawn_directions = [(-1, -1), (1, -1)]

        return check_directions({"Rook", "Queen"}, rook_directions, True) or \
               check_directions({"Bishop", "Queen"}, bishop_directions, True) or \
               check_directions({"Knight"}, knight_directions, False) or \
               check_directions({"King"}, king_directions, False) or \
               check_directions({"Pawn"}, pawn_directions, False)

    @property
    def king_checked(self):
        """
        Check if the king is checked on the board.
        :return: True if king is checked.
        """
        return self.is_checked(convert_index(self.table.index(get_piece("King", self.turn))))

    def make_move(self, (prev_x, prev_y), (next_x, next_y), promotion="Queen"):
        """
        Make one move on given board. It also changes the players turn.
        :param promotion: To which piece the pawn should promote.
        :return: Nothing?
        """
        new_table = list(self.table)

        def check_en_passant(new_table, x):
            return 0 <= x < 8 and \
                   new_table[convert_point((x, next_y))] == get_piece("Pawn", opposite_color(self.turn))

        previous = (prev_x, prev_y)
        next = (next_x, next_y)
        field_first = self.table[convert_point(previous)]
        field_second = self.table[convert_point(next)]
        if field_second is None or field_second.color != self.turn:
            new_table[convert_point(previous)] = None
            if field_first.piece_type == "Pawn":
                if next_y == 7 or next_y == 0:
                    new_table[convert_point(next)] = get_piece(promotion, self.turn)
                else:
                    new_table[convert_point(next)] = field_first
                if abs(prev_y - next_y) == 2:
                    if check_en_passant(new_table, prev_x - 1) or check_en_passant(new_table, prev_x + 1):
                        self.en_passant = prev_x
                    else:
                        self.en_passant = -1
            else:
                new_table[convert_point(next)] = field_first
        else:
            if self.turn == "White":
                row = 0
            else:
                row = 7
            new_table[convert_point(previous)] = None
            new_table[convert_point(next)] = None
            if prev_x == 0 or next_x == 0:
                new_table[convert_point((2, row))] = get_piece("King", self.turn)
                new_table[convert_point((3, row))] = get_piece("Rook", self.turn)
            else:
                new_table[convert_point((6, row))] = get_piece("King", self.turn)
                new_table[convert_point((5, row))] = get_piece("Rook", self.turn)
        self.turn = opposite_color(self.turn)
        self.table = new_table
        self.white_castle = (self.white_castle[0] and
                             previous != (4, 0) and
                             next != (4, 0) and
                             previous != (0, 0) and
                             next != (0, 0),
                             self.white_castle[1] and
                             previous != (4, 0) and
                             next != (4, 0) and
                             previous != (7, 0) and
                             next != (7, 0))
        self.black_castle = (self.white_castle[0] and
                             previous != (4, 7) and
                             next != (4, 7) and
                             previous != (0, 7) and
                             next != (0, 7),
                             self.white_castle[1] and
                             previous != (4, 7) and
                             next != (4, 7) and
                             previous != (7, 7) and
                             next != (7, 7))

    @property
    def can_castle(self):
        """
        Determines if the player whos turns it is can make a castle move.
        :return: Pair which describing both types of castles. King side and queen side. True means possibility of
        doing the castle.
        """
        if self.turn == "White":
            (queen_side, king_side) = self.white_castle
            row = 0
        else:
            (queen_side, king_side) = self.black_castle
            row = 7
        return queen_side and \
               self.table[convert_point((1, row))] is None and \
               self.table[convert_point((2, row))] is None and \
               self.table[convert_point((3, row))] is None and \
               not self.is_checked((2, row)) and \
               not self.is_checked((3, row)) and \
               not self.is_checked((4, row)), \
               king_side and \
               self.table[convert_point((5, row))] is None and \
               self.table[convert_point((6, row))] is None and \
               not self.is_checked((4, row)) and \
               not self.is_checked((5, row)) and \
               not self.is_checked((6, row))

    def possible_moves(self, (x, y)):
        """
        Generates all possible moves from given point. It should be calculated only
        once and then stored as a field in board. One should use get_moves instead of
        possible_moves.
        :return: List containing all possible moves from given point.
        """
        point = (x, y)

        def check_direction(direction, slide):
            moves = []
            current_point = add_vectors(point, direction)
            while check_bounds(current_point):
                field = self.table[convert_point(current_point)]
                if field is None:
                    moves += [(point, current_point)]
                elif field.color != self.turn:
                    moves += [(point, current_point)]
                    break
                else:
                    break
                if not slide:
                    break
                current_point = add_vectors(current_point, direction)
            return moves

        def check_directions(directions, slide):
            moves = []
            for direction in directions:
                moves += check_direction(direction, slide)
            return moves

        field = self.table[convert_point(point)]
        officers = ["Bishop", "Knight", "Rook", "Queen"]
        if field is None or field.color != self.turn:
            return []
        if field.piece_type == "Pawn":
            # No capture moves.
            moves = []
            if self.turn == "White":
                delta = (0, 1)
            else:
                delta = (0, -1)
            next = add_vectors(point, delta)
            next_field = self.table[convert_point(next)]
            if check_bounds(next) and next_field is None:
                if next[1] == 0 or next[1] == 7:
                    moves += map(lambda officer: (point, next, officer), officers)
                else:
                    moves += [(point, next)]
            if (y == 1 and self.turn == "White") or (y == 6 and self.turn == "Black"):
                temp_field = next_field
                next = add_vectors(next, delta)
                next_field = self.table[convert_point(next)]
                if temp_field is None and next_field is None:
                    moves += [(point, next)]

            # Capture moves
            def check_column(dx):
                next = add_vectors(point, (dx, delta[1]))
                next_field = self.table[convert_point(next)]
                if check_bounds(next):
                    if next_field is None:
                        if self.en_passant == next[0] and \
                                ((next[1] == 5 and self.turn == "White") or \
                                         (next[1] == 2 and self.turn == "Black")):
                            return [(point, next)]
                    elif next_field.color != self.turn:
                        if next[1] == 0 or next[1] == 7:
                            return map(lambda officer: (point, next, officer), officers)
                        else:
                            return [(point, next)]
                return []

            moves += check_column(-1)
            moves += check_column(1)
            return moves
        else:
            moves = []
            if self.turn == "White":
                row = 0
            else:
                row = 7
            if field.piece_type == "King" or field.piece_type == "Rook":
                (queen_side, king_side) = self.can_castle
                if king_side:
                    moves += [((4, row), (7, row))]
                if queen_side:
                    moves += [((4, row), (0, row))]
            return moves + check_directions(field.directions, field.slide)

    def recalculate_moves(self):
        """
        Recalculate all possible moves that can be done from each field.
        """

        def check_move(move):
            promotion = "Queen"
            if len(move) == 2:
                (previous, next) = move
            else:
                (previous, next, promotion) = move
            new = copy.copy(self)
            new.table = copy.copy(self.table)
            new.turn = copy.copy(self.turn)
            new.white_castle = copy.copy(self.white_castle)
            new.black_castle = copy.copy(self.black_castle)
            new.en_passant = copy.copy(self.en_passant)
            new.make_move(previous, next, promotion)
            new.turn = opposite_color(new.turn)
            return not new.king_checked

        self.win = opposite_color(self.turn)
        for i in range(64):
            self.moves[i] = filter(check_move, self.possible_moves(convert_index(i)))
            if self.moves[i]:
                self.win = None

    def get_moves(self, point):
        """
        Get possible moves from given point. This uses previously cached informations.
        :param point: Point from which
        :return: All possible moves that can be done from given point.
        """
        return self.moves[convert_point(point)]
