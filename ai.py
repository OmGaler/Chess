import random


### active
#todo don't move pieces intentionally into harms way - see if square to move to is in legal moves of enemy piece - won't work for pawn, king
#fixme: current algorithm doesn't work for pawns as it assumes that the protecting piece would be able to move there if the square is empty
#todo: tactics priority: 1. checkmate 2. promote (if feasible), 3. capture 4. make sure you're not blundering your piece away

### on hold
#todo: see if a checkmate is available!! --on hold
#fixme cant play against white AI
#optimise: change iterating over lists to generators, its much more efficient and at this point it would be flipping idiotic not to do that
#optimise: fix latency between human move showing and ai move showing -better there is a delay when ai moves (after human's piece has moved)
#fixme insufficient material bug - both players must have insufficient material
#fixme pawn next to king (NOT CHECKING) sometimes goes red, also king can;t move when a piece is pinned to it


# [x]  #lvl 1 - random move generation 
#      #lvl 2 - move with simple strategies e/g
            #checkmating where possible
            #capturing where possible to gain most favourable material situation
#     #lvl 3 - minimax algorithm utilising trees and alpha-beta pruning


material_points = {None: 0,
                   "Pawn":   1,
                   "Knight": 3,
                   "Bishop": 3,
                   "Rook":   5,
                   "Queen":  9,
                   "King": 100}

def makeMove(lvl, pieces, turn, board=None): #decides which algorithm will make the move
    #makeshift case statement to run required level of AI
    {1: AIlvl1,
     2: AIlvl2,
     3: AIlvl3} [lvl] (pieces, turn, board) #run required function with parameters

#AI Lvl 1: The simplest of all algorithms - computer selects and makes a random legal move
def AIlvl1(pieces, turn, board):
    possible_moves = { } #dictionary to hold possible moves, each piece is a key with its respective moves as items
    for piece in [x for x in pieces if x.colour==turn]: #iterating over all the player's pieces
        piece.legalMoves()
        piece.illegalMoves()
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
def AIlvl2(pieces, turn, board): #ai powered with simple strategy
    possible_moves = {}  #dictionary to hold possible moves, each piece is a key with its respective moves as items
    possible_captures = {}  #dictionary to hold all possible captures so the capture with greatest gain in material can be captured
    for piece in (x for x in pieces if x.colour == turn):  #iterating over all the player's pieces
        piece.legalMoves()
        piece.illegalMoves()
        possible_moves[piece] = []
        for p in piece.legal_moves:  #iterating over that piece's legal moves
            possible_moves[piece].append(p)



            protected_squares = {x: [None] for x in board} #keeping track of pieces that defend each square
            for w in (v for v in pieces if v.colour != turn):
                if p in w.legal_moves:
                    if protected_squares[p] is None:
                        protected_squares[p] = type(piece).__name__
                    else:
                        protected_squares[p].append(type(piece).__name__)
                    #print(protected_squares)
            ###################################################################################################
            #todo check for checkmate
            '''
            for m in (n for n in pieces if n.colour != turn):
                m.legalMoves()
                m.illegalMoves()
            for c in (d for d in pieces if d.colour != turn):
                if type(c).__name__ is "King":
                    if c.position in piece.legal_moves:
                        #if type(m).__name__ is "King" and m.position in piece.legal_moves:  #checking for check
                        #checking if there are any legal moves
                        for a in (b for b in pieces if b.colour != turn):
                            a.legalMoves()
                            a.illegalMoves()
                            if len(a.legal_moves) != 0:
                                break
                        else:
                            pieceToMove = piece
                            moveToMake = p
                            pieceToMove.makeMove(moveToMake)
                            print("Checkmate!!!!!")
                            return
                    break

                if p in m.legal_moves:
                    protectors.append(type(m).__name__)
            '''

            if board[p]["text"] != "":  #move involves capturing an enemy piece
                tempText = board[p].text
                board[p]["text"] = ""  ##take off
                board[p].text = ""
                #generate a list of pieces protecting each square
                score = material_points[board[p].occupier]
                protectors = []

                for m in (n for n in pieces if n.colour != turn):
                    m.legalMoves()
                    m.illegalMoves()
                    if p in m.legal_moves:
                        protectors.append(type(m).__name__)

                possible_captures[piece] = (p, score, (score - material_points[type(piece).__name__]),
                                            protectors)  ##(p, score, netChangeInMaterial, underThreatBy)
                ##IMPORTANT - THIS DOES NOT WORK FOR PAWNS AS THEY WONT BE ABLE TO MOVE THERE IF THERE IS NO PIECE
                ##ALSO ONLY WORKS FOR ONE THREATENING PIECE, not necessarily the least valuable
                ###
                ######but why???

                board[p]["text"] = tempText  ##take off
                board[p].text = tempText


    #check for promotions
    for piece in possible_moves:
        if type(piece).__name__ is "Pawn":
            for move in possible_moves[piece]:
                if move[1] in ["1","8"]:  #pawn has reached the last rank
                    #the promotion square is not defended so pawn would not be captured upon promotion
                    pieceToMove = piece
                    moveToMake = move
                    pieceToMove.move(moveToMake)
                    return



    if len(possible_captures) > 0:  #at least one capture can be made
        #sorting the dictionary of possible captures so moves are ordered by how good they are
        for p in possible_captures:
            if len(possible_captures[p][3]) > 0:  #at least one piece is defending so evaluate the net change in
                # material assuming the capturing piece will be lost
                try:
                    possible_captures_sorted = {x: y for x, y in sorted(possible_captures.items(),
                                                                        key=lambda item: ((item[1][1]), item[1][2]),
                                                                        reverse=True)}

                    #if c-a negative don't make move
                except KeyError:
                    continue
                """secondary sorting index = score of capture - score of capturing piece"""
                #sort first based on value of piece being taken and then on whether
                # the captured piece is protected by another piece and then by the value of the capturing piece
                #When I wrote the above line, only G-d and I knew what I was talking about. Now only G-d knows
                break

        else:
            possible_captures_sorted = {x: y for x, y in
                                        sorted(possible_captures.items(), key=lambda item: (item[1][1]),
                                               reverse=True)}

        #promote a pawn if the promoted piece will not be immediately captured
        for y in possible_captures_sorted:
            if type(y).__name__ is "Pawn" and possible_captures_sorted[y][0][1] in ["1","8"]:  #pawn has reached the last rank
                #the promotion square is not defended so pawn would not be captured upon promotion
                if len(possible_captures_sorted[y][3]) == 0:
                    pieceToMove = y
                    moveToMake = possible_captures_sorted[y][0]
                    pieceToMove.move(moveToMake)
                    return

        #finding first entry in dictionary -make capture that results in greatest material gain
        for x in possible_captures_sorted:
            if len(possible_captures_sorted[x][3]) > 0:  #the piece to be captured is defended
                if possible_captures_sorted[x][2] < 0:  #and there is a net loss in material so skip the move
                    del possible_moves[x][0]
                    continue
            pieceToMove = x  #piece to be moved
            moveToMake = possible_captures_sorted[x][0]
            pieceToMove.move(moveToMake)  #makes the move
            break
        else:
            AIlvl1(pieces, turn, board)
    else:  #no captures available so select a random move
        #for piece in possible_moves: #remove moves in which a piece is blundered away
            #for move in possible_moves[piece]:
                #if len(protected_squares[move]) > 1:
                    #del possible_moves[piece][move]
        AIlvl1(pieces, turn, board)  #in hindsight this is a terrible strategy





#AI Lvl 3: The most complex of all algorithms - utilises minimax algorithm implemented with a game tree
def AIlvl3(pieces, turn, board):
    def evaluate(): #evaluates state of the board
        pass
    def minimax():
        pass
    #optimise: alpha-beta pruning
    raise ValueError("still in development :/")