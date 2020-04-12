
import chess
import random

def randMove():
    possible_moves = { }
    for piece in chess.Pieces.pieces:
        print("success#2")
        print(piece)
        piece.legalMoves()
        possible_moves[piece] = [ ]
        for p in piece.legal_moves:
            possible_moves[piece].append(p)
    print(chess.Pieces.pieces)
    pieceToMove = random.randint(0, len(chess.Pieces.pieces)-1)
    possible_moves[pieceToMove].shuffle()
    moveToMake = possible_moves[pieceToMove][0]
    pieceToMove.move(moveToMake)

'''two way import doesnt work?'''