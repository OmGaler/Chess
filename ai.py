<<<<<<< HEAD
import random


def makeMove(lvl, pieces, turn): #decides which algorithm will make the move
    #makeshift case statement to run required level of AI
    {1: AIlvl1(pieces, turn),
     2: error,
     3: error} [lvl]

#AI Lvl 1: The simplest of all algorithms - computer selects and makes a random legal move
def AIlvl1(pieces, turn):
    possible_moves = { } #dictionary to hold possible moves, each piece is a key with its respective moves as items
    for piece in [x for x in pieces if x.colour==turn]: #iterating over all the player's pieces
        piece.legalMoves()
        possible_moves[piece] = [ ]
        for p in piece.legal_moves: #iterating over that piece's legal moves
            possible_moves[piece].append(p)
    #selecting a random legal move
    while True:
        piece_move = random.sample(possible_moves.items(), 1) #selects a random piece and a random move for that piece
        piece_move = list(map(list, piece_move))[0]
        if len(piece_move[1]) == 0: #piece has no valid moves so can't be moved, another piece must be selected
            continue
        else: #piece has at least one valid move
            piece_move[1] = random.choice(piece_move[1]) #if this piece has more than one
            # legal move, selects a random move and discard the rest
            break
    pieceToMove = piece_move[0] #piece to be moved
    moveToMake = piece_move[1] #where the piece will be moved to
    pieceToMove.move(moveToMake) #makes the move

#AI Lvl 2
def AIlvl2(pieces, turn):
    pass

#AI Lvl 3: The most complex of all algorithms
def AIlvl3(pieces, turn):
    pass

def error():
    raise ValueError("still in development :/")
=======

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
>>>>>>> refs/remotes/origin/master
