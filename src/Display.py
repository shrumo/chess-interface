__author__ = 'Maksymilian Mika'

import Chess
import pygame


class BoardDisplay:
    def __init__(self):
        """
        Initialize images and create beginning board. Also recalculate the moves that
        can be done on the board.
        """
        self.field_width = 60
        self.field_height = 60
        self.width = self.field_width * 8
        self.height = self.field_height * 8
        self.board = Chess.Board()
        self.board.recalculate_moves()

        # Change to prettier fields
        self.white_field = pygame.Surface((self.field_width, self.field_height))
        self.white_field.fill((245, 222, 179))

        # Change to prettier fields.
        self.black_field = pygame.Surface((self.field_width, self.field_height))
        self.black_field.fill((205, 133, 63))

        self.move_field = pygame.Surface((self.field_width, self.field_height))
        self.move_field.fill((139, 0, 0))
        self.move_field.set_alpha(115)

        self.pieces = []
        index = 0
        for field in self.board.table:
            if field is not None:
                self.pieces.append(Piece(field, Chess.convert_index(index)))
            index += 1

        self.dragged_piece = None
        self.possible_moves = []

        self.opaque = 0

        self.white_wins = pygame.image.load("res/white_wins.png")
        self.black_wins = pygame.image.load("res/black_wins.png")

    def display(self, screen):
        """
        Display current status of the board.
        :param screen: Screen on which the board is to be displayed.
        """
        for i in range(64):
            (x, y) = Chess.convert_index(i)
            if (x + y) % 2 == 0:
                screen.blit(self.white_field, (x * self.field_width, y * self.field_height))
            else:
                screen.blit(self.black_field, (x * self.field_width, y * self.field_height))
        for move in self.possible_moves:
            if len(move) == 2:
                (previous, next) = move
                screen.blit(self.move_field, (previous[0] * self.field_width, previous[1] * self.field_height))
                screen.blit(self.move_field, (next[0] * self.field_width, next[1] * self.field_height))
            else:
                (previous, next, promotion) = move
                screen.blit(self.move_field, (previous[0] * self.field_width, previous[1] * self.field_height))
                screen.blit(self.move_field, (next[0] * self.field_width, next[1] * self.field_height))
        for piece in self.pieces:
            piece.display(screen)
        if self.board.win is not None:
            self.opaque += 3
            if self.opaque > 225:
                self.opaque = 225
            surface = pygame.Surface((self.width, self.height))
            if self.board.win == "White":
                surface.fill((255, 255, 255))
            else:
                surface.fill((0, 0, 0))
            surface.set_alpha(self.opaque)
            screen.blit(surface, (0, 0))
            if self.board.win == "White":
                screen.blit(self.white_wins, (0, 0))
            else:
                screen.blit(self.black_wins, (0, 0))

    def find_field(self, pos):
        """
        Find the piece that is on the given position.
        :param pos: Position of searched piece.
        :return: Piece on that position or None if there is none.
        """
        for piece in self.pieces:
            if piece.position == pos:
                return piece
        return None

    def dragged(self, p):
        """
        This means that someone is dragging the thing that is on (x,y).
        """
        x,y = p
        if self.board.win is not None:
            return
        x //= self.field_width
        y //= self.field_height
        self.possible_moves = self.board.get_moves((x, y))
        if not self.possible_moves:
            return
        field = self.find_field((x, y))
        if field is not None:
            field.dragged = True
            self.dragged_piece = field

    def dropped(self, p):
        """
        This means that someone dropped the dragged thing on (x,y).
        """
        x,y = p
        if self.board.win is not None:
            return
        x //= self.field_width
        y //= self.field_height
        if self.dragged_piece is not None and ((self.dragged_piece.position, (x, y)) in self.possible_moves \
                                                       or (
                    self.dragged_piece.position, (x, y), "Queen") in self.possible_moves):
            self.board.make_move(self.dragged_piece.position, (x, y))
            print(str(self.dragged_piece.position) + " " + str((x, y)))
            print(self.board)
            self.pieces = []
            index = 0
            for field in self.board.table:
                if field is not None:
                    self.pieces.append(Piece(field, Chess.convert_index(index)))
                index += 1
            self.board.recalculate_moves()
            self.dragged_piece.dragged = False
            self.dragged_piece = None
            self.possible_moves = []
        elif self.dragged_piece is not None:
            self.dragged_piece.dragged = False
            self.dragged_piece = None


class Piece:
    def __init__(self, piece, point):
        """
        Initialize the given piece and load it image.
        :param piece: Piece type.
        """
        x,y = point
        if piece == Chess.white_pawn:
            self.image = pygame.image.load("res/white_pawn.png")
        elif piece == Chess.white_rook:
            self.image = pygame.image.load("res/white_rook.png")
        elif piece == Chess.white_knight:
            self.image = pygame.image.load("res/white_knight.png")
        elif piece == Chess.white_king:
            self.image = pygame.image.load("res/white_king.png")
        elif piece == Chess.white_queen:
            self.image = pygame.image.load("res/white_queen.png")
        elif piece == Chess.white_bishop:
            self.image = pygame.image.load("res/white_bishop.png")
        elif piece == Chess.black_pawn:
            self.image = pygame.image.load("res/black_pawn.png")
        elif piece == Chess.black_rook:
            self.image = pygame.image.load("res/black_rook.png")
        elif piece == Chess.black_knight:
            self.image = pygame.image.load("res/black_knight.png")
        elif piece == Chess.black_king:
            self.image = pygame.image.load("res/black_king.png")
        elif piece == Chess.black_queen:
            self.image = pygame.image.load("res/black_queen.png")
        elif piece == Chess.black_bishop:
            self.image = pygame.image.load("res/black_bishop.png")
        self.dragged = False
        self.position = (x, y)

    def display(self, screen):
        """
        Display the piece on the screen.
        :param screen: Screen to display on.
        """
        if self.dragged:
            screen.blit(self.image, (pygame.mouse.get_pos()[0] - self.image.get_width() // 2,
                                     pygame.mouse.get_pos()[1] - self.image.get_height() // 2))
        else:
            screen.blit(self.image,
                        (self.position[0] * self.image.get_width(),
                         self.position[1] * self.image.get_height()))
