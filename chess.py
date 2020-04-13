##!/usr/bin/python
#Chess
#Omer Galer
#2018

#importing modules

import math, winsound, webbrowser
import gc #importing a module to find instances - i.e. find pieces by location
import ai

try:
    from tkinter import * #import tkinter module for the GUI, python 3.x
    from tkinter import messagebox
except ImportError:
    from Tkinter import * #python 2.x
    from Tkinter import messagebox


#Piece classes - each individual piece is an instance of this class
class Pieces:

    #class attributes - not specific to each piece
    moves = [""]
    captured = [ ]
    pieces = [ ]
    captured_icons = [ ]
    #initialising instances
    def __init__(self, root, frame, grid, colour, board):
        self.root = root
        self.grid = grid
        self.colour = colour
        self.frame = frame
        self.legal_moves = [ ]
        self.board = board
        self.moveCounter = 0
        #variables for specific piece types
        if type(self).__name__ is "Pawn":
            self.enPassant = False
        elif type(self).__name__ is "King":
            self.castling = False

        self.__class__.pieces.append(self) #keeping track of all the pieces in a list
        self.alph = ["a", "b", "c", "d", "e", "f", "g", "h"]
        #creating a map from numeric to alpha notation and vice versa
        self.file_rank = {a: b+1 for a, b in zip(self.alph, range(8))}
        self.rank_file = {y: z for z, y in self.file_rank.items()}
        if len(self.pieces) == 1:
            #mapping piece name+colour to piece icon
            Pieces.WK = u"♔"
            Pieces.WQ = u"♕"
            Pieces.WN = u"♘"
            Pieces.WB = u"♗"
            Pieces.WR = u"♖"
            Pieces.WP = u"♙"

            Pieces.BK = u"♚"
            Pieces.BQ = u"♛"
            Pieces.BN = u"♞"
            Pieces.BB = u"♝"
            Pieces.BR = u"♜"
            Pieces.BP = u"♟"
            
            Pieces.texts = [Pieces.WK, Pieces.WQ, Pieces.WR, Pieces.WB, Pieces.WN, Pieces.WP, "", \
                            Pieces.BK, Pieces.BQ, Pieces.BR, Pieces.BB, Pieces.BN, Pieces.BP]
            Pieces.text = ["wK", "wQ", "wR", "wB", "wN", "wP", "", "bK", "bQ", "bR", "bB", "bN", "bP"]
            Pieces.dct1 = dict(zip(Pieces.texts, Pieces.text)) #mapping dictionaries
            Pieces.dct2 = dict(zip(Pieces.text, Pieces.texts))


    def legalMoves(self): #generates a list of legal moves for the piece which it is called by
        #making a local variable for keeping track of both kings
        self.wKing = [x for x in self.pieces if type(x).__name__ == "King" and x.colour == "W"][0]
        self.bKing = [x for x in self.pieces if type(x).__name__ == "King" and x.colour == "B"][0]

        self.legal_moves = [ ] #initialising an empty list to hold all legal moves for this piece
        file = int(self.position[0]) #current position of piece; file is the column (a-h)
        rank = int(self.position[1]) #and rank is the row (1-8)

        if type(self).__name__ is "Pawn": #legal moves for a pawn
            #pawn's legal moves (excluding captures) consists of one square forward at a time, optional two squares only
            #starting position; captures are made diagonally forwards only
            #if a pawn reaches the last rank (1st for black, 8th for white) it promotes to a piece (Knight/Bishop/Rook/
            #Queen) of the player's choosing
            if (self.colour == "W" and rank == 8) or (self.colour == "B" and rank == 1): #
                return #pawn has reached end of board and is eligible for promotion

            if self.colour == "W": #white pawns move up ranks
                if rank == 2 and self.dct1[self.board[str(file) + str(rank+1)].text] == "":
                    if self.dct1[self.board[str(file) + str(rank+2)].text] == "":
                        self.legal_moves.append(str(file) + str(rank+2))#pawn can move two squares from its starting pos
                    self.legal_moves.append(str(file) + str(rank+1)) #pawn's move is one step forward
                elif rank != 2 and self.dct1[self.board[str(file) + str(rank+1)].text] == "":
                    self.legal_moves.append(str(file) + str(rank+1)) #pawn's move is one step forward
                #captures
                try: #pawns capture enemy piece diagonally forward
                    if "b" in self.dct1[self.board[str(file+1) + str(rank+1)].text]:
                        self.legal_moves.append(str(file+1) + str(rank+1))
                except: pass
                try:
                    if "b" in self.dct1[self.board[str(file-1) + str(rank+1)].text]:
                        self.legal_moves.append(str(file-1) + str(rank+1))
                except: pass
            else: #black pawns move down ranks
                if rank == 7 and self.dct1[self.board[str(file) + str(rank-1)].text] == "":
                    if self.dct1[self.board[str(file) + str(rank-2)].text] == "":
                        self.legal_moves.append(str(file) + str(rank-2))#pawn can move two squares from its starting pos
                    self.legal_moves.append(str(file) + str(rank-1)) #pawn's move is one step forward
                elif rank != 7 and self.dct1[self.board[str(file) + str(rank-1)].text] == "":
                    self.legal_moves.append(str(file) + str(rank-1)) #pawn's move is one step forward
                #captures
                try: #pawns capture enemy piece diagonally forward
                    if "w" in self.dct1[self.board[str(file+1) + str(rank-1)].text]:
                        self.legal_moves.append(str(file+1) + str(rank-1))
                except: pass
                try:
                    if "w" in self.dct1[self.board[str(file-1) + str(rank-1)].text]:
                        self.legal_moves.append(str(file-1) + str(rank-1))
                except: pass

            #enabling en-passant - if a pawn makes a double-step move from its starting position and an enemy pawn is
            #in a position such that had the pawn not double-stepped it could have been captured, the enemy pawn is able
            #to capture the pawn "en-passant" in passing - the pawn is captured but the enemy pawn does not occupy the
            #same sqaure as normal, rather it goes to the square the pawn would have moved to had it not double-stepped
            #i.e. behind the captured pawn on the same file
            if len(self.moves) > 1:
                for v in [u for u in self.pieces if u.colour != self.colour and type(u).__name__ is "Pawn"]:
                    #finding pawns that have made a double-step move in the preceding move
                    if v.colour == "W" and v.position[1] == "4" and v.moveCounter == 1 \
                       and self.position[1] == v.position[1] and \
                       self.moves[-1] == str(self.rank_file[int(v.position[0])])+"4":
                        self.legal_moves.append(v.position[0]+str(int(v.position[1])-1))
                        self.enPassant = True
                    elif v.colour == "B" and v.position[1] == "5" and v.moveCounter == 1 \
                         and self.position[1] == v.position[1] and \
                           self.moves[-1] == str(self.rank_file[int(v.position[0])])+"5":
                        self.legal_moves.append(v.position[0]+str(int(v.position[1])+1))
                        self.enPassant = True

        elif type(self).__name__ is "Knight": #legal moves for a knight
            #knight's legal moves consist of two squares in one direction and one square in a perpendicular direction
            # (L-shape). The knight, unlike other pieces, can jump over other pieces
            if file + 1 < 9 and rank + 2 < 9: #8 possibilities of l-shaped moves
                self.legal_moves.append(str(file+1) + str(rank+2))
            if file + 2 < 9 and rank + 1 < 9:
                self.legal_moves.append(str(file+2) + str(rank+1))
            if file + 1 < 9 and rank - 2 > 0:
                self.legal_moves.append(str(file+1) + str(rank-2))
            if file + 2 < 9 and rank - 1 > 0:
                self.legal_moves.append(str(file+2) + str(rank-1))
            if file - 1 > 0 and rank + 2 < 9:
                self.legal_moves.append(str(file-1) + str(rank+2))
            if file - 2 > 0 and rank + 1 < 9:
                self.legal_moves.append(str(file-2) + str(rank+1))
            if file - 1 > 0 and rank - 2 > 0:
                self.legal_moves.append(str(file-1) + str(rank-2))
            if file - 2 > 0 and rank - 1 > 0:
                self.legal_moves.append(str(file-2) + str(rank-1))
            illegal = [ ]
            #illegalising moves to squares which already contain a piece of the same colour
            for k in self.legal_moves:
                if self.colour.lower() in self.dct1[self.board[k].text]: #friendly piece resides in that position
                    illegal.append(k)
            for m in illegal:
                self.legal_moves.remove(m)

        elif type(self).__name__ is "Rook": #legal moves for a rook
            #rook's legal moves consist of unlimited horizontal and vertical movement along each rank or file until a
            #piece is encountered, if the piece is an opponent that piece may be captured and the rook may move no
            #further, if the piece is friendly that position may not be taken and the rook may move no further
            counter = [False] * 4 #counters to keep track of direction that is being iterated over
            for i in range(1, 9): #max 8 ranks, 8 files
                if file+i < 9 and counter[0] is False: #file is on board
                    x = str(file+i) + str(rank)
                    if self.colour.lower() not in self.dct1[self.board[x].text]:
                        if self.dct1[self.board[x].text] != "":
                            self.legal_moves.append(x) #move is valid
                            counter[0]=True #move to next direction; rook can move no further
                        else:
                            self.legal_moves.append(x) #move is valid
                    else:
                        counter[0]=True #move to next direction; rook can move no further

                if rank+i < 9 and counter[1] is False: #rank is on board
                    x = str(file) + str(rank+i)
                    if self.colour.lower() not in self.dct1[self.board[x].text]:
                        if self.dct1[self.board[x].text] != "":
                            self.legal_moves.append(x) #move is valid
                            counter[1]=True #move to next direction; rook can move no further
                        else:
                            self.legal_moves.append(x) #move is valid
                    else:
                        counter[1]=True #move to next direction; rook can move no further

                if file-i > 0 and counter[2] is False: #file is on board
                    x = str(file-i) + str(rank)
                    if self.colour.lower() not in self.dct1[self.board[x].text]:
                        if self.dct1[self.board[x].text] != "":
                            self.legal_moves.append(x) #move is valid
                            counter[2]=True #move to next direction; rook can move no further
                        else:
                            self.legal_moves.append(x) #move is valid
                    else:
                        counter[2]=True #move to next direction; rook can move no further

                if rank-i > 0 and counter[3] is False: #rank is on board
                    x = str(file) + str(rank-i)
                    if self.colour.lower() not in self.dct1[self.board[x].text]:
                        if self.dct1[self.board[x].text] != "":
                            self.legal_moves.append(x) #move is valid
                            counter[3]=True #move to next direction; rook can move no further
                        else:
                            self.legal_moves.append(x) #move is valid
                    else:
                        counter[3]=True #move to next direction; rook can move no further

        elif type(self).__name__ is "Bishop": #legal moves for a bishop
        #bishop's legal moves consist of unlimited diagonal movement along diagonals of the same colour
        #until a piece is encountered, if the piece is an opponent that piece may be captured and the bishop may move
        #no further, if the piece is friendly that position may not be taken and the bishop may move no further
            counter = [False] * 4 #counters to keep track of direction that is being iterated over
            for j in range(1,9): #max 8 squares on each diagonal
                if file+j < 9 and rank+j < 9 and counter[0] is False: #file and rank are on board
                    x = str(file+j) + str(rank+j)
                    if self.colour.lower() not in self.dct1[self.board[x].text]:
                        if self.dct1[self.board[x].text] != "":
                            self.legal_moves.append(x) #move is valid
                            counter[0]=True #move to next direction; bishop can move no further
                        else:
                            self.legal_moves.append(x) #move is valid
                    else:
                        counter[0]=True #move to next direction; bishop can move no further

                if file-j > 0 and rank-j > 0 and counter[1] is False: #file and rank are on board
                    x = str(file-j) + str(rank-j)
                    if self.colour.lower() not in self.dct1[self.board[x].text]:
                        if self.dct1[self.board[x].text] != "":
                            self.legal_moves.append(x) #move is valid
                            counter[1]=True #move to next direction; bishop can move no further
                        else:
                            self.legal_moves.append(x) #move is valid
                    else:
                        counter[1]=True #move to next direction; bishop can move no further

                if file+j < 9 and rank-j > 0 and counter[2] is False: #file and rank are on board
                    x = str(file+j) + str(rank-j)
                    if self.colour.lower() not in self.dct1[self.board[x].text]:
                        if self.dct1[self.board[x].text] != "":
                            self.legal_moves.append(x) #move is valid
                            counter[2]=True #move to next direction; bishop can move no further
                        else:
                            self.legal_moves.append(x) #move is valid
                    else:
                        counter[2]=True #move to next direction; bishop can move no further

                if file-j > 0 and rank+j < 9 and counter[3] is False: #file and rank are on board
                    x = str(file-j) + str(rank+j)
                    if self.colour.lower() not in self.dct1[self.board[x].text]:
                        if self.dct1[self.board[x].text] != "":
                            self.legal_moves.append(x) #move is valid
                            counter[3]=True #move to next direction; bishop can move no further
                        else:
                            self.legal_moves.append(x) #move is valid
                    else:
                        counter[3]=True #move to next direction; bishop can move no further


        elif type(self).__name__ is "Queen":
            #queen's legal moves consist of unlimited horizontal, vertical and diagonal
            #movement, i.e. combining the moves of the rook and the bishop
            counter = [False] * 4 #counters to keep track of direction that is being iterated over
            for i in range(1, 9): #max 8 ranks, 8 files
                if file+i < 9 and counter[0] is False: #file is on board
                    x = str(file+i) + str(rank)
                    if self.colour.lower() not in self.dct1[self.board[x].text]:
                        if self.dct1[self.board[x].text] != "":
                            self.legal_moves.append(x) #move is valid
                            counter[0]=True #move to next direction; queen can move no further
                        else:
                            self.legal_moves.append(x) #move is valid
                    else:
                        counter[0]=True #move to next direction; queen can move no further

                if rank+i < 9 and counter[1] is False: #rank is on board
                    x = str(file) + str(rank+i)
                    #try:
                    if self.colour.lower() not in self.dct1[self.board[x].text]:
                        if self.dct1[self.board[x].text] != "":
                            self.legal_moves.append(x) #move is valid
                            counter[1]=True #move to next direction; queen can move no further
                        else:
                            self.legal_moves.append(x) #move is valid
                    else:
                        counter[1]=True #move to next direction; queen can move no further

                if file-i > 0 and counter[2] is False: #file is on board
                    x = str(file-i) + str(rank)
                    #try:
                    if self.colour.lower() not in self.dct1[self.board[x].text]:
                        if self.dct1[self.board[x].text] != "":
                            self.legal_moves.append(x) #move is valid
                            counter[2]=True #move to next direction; queen can move no further
                        else:
                            self.legal_moves.append(x) #move is valid
                    else:
                        counter[2]=True #move to next direction; queen can move no further

                if rank-i > 0 and counter[3] is False: #rank is on board
                    x = str(file) + str(rank-i)
                    if self.colour.lower() not in self.dct1[self.board[x].text]:
                        if self.dct1[self.board[x].text] != "":
                            self.legal_moves.append(x) #move is valid
                            counter[3]=True #move to next direction; queen can move no further
                        else:
                            self.legal_moves.append(x) #move is valid
                    else:
                        counter[3]=True #move to next direction; queen can move no further

            counter = [False] * 4 #counters to keep track of direction that is being iterated over
            for j in range(1,9):
                if file+j < 9 and rank+j < 9 and counter[0] is False: #file and rank are on board
                    x = str(file+j) + str(rank+j)
                    if self.colour.lower() not in self.dct1[self.board[x].text]:
                        if self.dct1[self.board[x].text] != "":
                            self.legal_moves.append(x) #move is valid
                            counter[0]=True #move to next direction; queen can move no further
                        else:
                            self.legal_moves.append(x) #move is valid
                    else:
                        counter[0]=True #move to next direction; queen can move no further

                if file-j > 0 and rank-j > 0 and counter[1] is False: #file and rank are on board
                    x = str(file-j) + str(rank-j)
                    if self.colour.lower() not in self.dct1[self.board[x].text]:
                        if self.dct1[self.board[x].text] != "":
                            self.legal_moves.append(x) #move is valid
                            counter[1]=True #move to next direction; queen can move no further
                        else:
                            self.legal_moves.append(x) #move is valid
                    else:
                        counter[1]=True #move to next direction; queen can move no further

                if file+j < 9 and rank-j > 0 and counter[2] is False: #file and rank are on board
                    x = str(file+j) + str(rank-j)
                    if self.colour.lower() not in self.dct1[self.board[x].text]:
                        if self.dct1[self.board[x].text] != "":
                            self.legal_moves.append(x) #move is valid
                            counter[2]=True #move to next direction; queen can move no further
                        else:
                            self.legal_moves.append(x) #move is valid
                    else:
                        counter[2]=True #move to next direction; queen can move no further

                if file-j > 0 and rank+j < 9 and counter[3] is False: #file and rank are on board
                    x = str(file-j) + str(rank+j)
                    if self.colour.lower() not in self.dct1[self.board[x].text]:
                        if self.dct1[self.board[x].text] != "":
                            self.legal_moves.append(x) #move is valid
                            counter[3]=True #move to next direction; queen can move no further
                        else:
                            self.legal_moves.append(x) #move is valid
                    else:
                        counter[3]=True #move to next direction; queen can move no further

        elif type(self).__name__ is "King":
            #king's legal moves consist of movement of one square in any direction
            #however the king cannot be moved into the path of an opponent piece such that it could be captured on the
            #next move; similarly, any other piece cannot be moved if it opens the king up to direct attack
            if file + 1 < 9 and rank + 1 < 9: #8 possible directions/moves
                self.legal_moves.append(str(file+1) + str(rank+1))
            if file + 1 < 9 and rank - 1 > 0:
                self.legal_moves.append(str(file+1) + str(rank-1))
            if file - 1 > 0 and rank + 1 < 9:
                self.legal_moves.append(str(file-1) + str(rank+1))
            if file - 1 > 0 and rank - 1 > 0:
                self.legal_moves.append(str(file-1) + str(rank-1))
            if file + 1 < 9:
                self.legal_moves.append(str(file+1) + str(rank))
            if file - 1 > 0:
                self.legal_moves.append(str(file-1) + str(rank))
            if rank + 1 < 9:
                self.legal_moves.append(str(file)+ str(rank+1))
            if rank - 1 > 0:
                self.legal_moves.append(str(file) + str(rank-1))
            illegal = [ ]
            #illegalising moves to squares which already contain a piece of the same colour
            for k in self.legal_moves:
                if self.colour.lower() in self.dct1[self.board[k].text]:
                    illegal.append(k)
            for m in illegal:
                self.legal_moves.remove(m)

            #castling
            if "+" not in self.moves[-1]: #king isn't in check; castling is permitted
                if self.moveCounter == 0: #king cannot have moved to castle
                    if self.colour == "W": #castling takes place on 1st rank (white castles)
                        #kingside
                        for f in ["61", "71"]:
                            try:
                                for piece in [k for k in self.pieces if k.colour != self.colour]:
                                    if f in piece.legal_moves:
                                        raise StopIteration() #king cannot pass through check while castling
                                    if self.dct1[self.board[f].text] != "": #no pieces can be in between king and rook
                                        raise StopIteration() #StopIteration exception is used here to break out of a
                            except StopIteration:                                          #double (nested) for-loop
                                break
                        else:
                            try:
                                rook = [h for h in self.pieces if h.colour == self.colour and type(h).__name__ is \
                                        "Rook" and h.position == "81"][0] #finding a rook with which to castle
                                for piece in [t for t in self.pieces if t.colour != self.colour]:
                                    #rook can't have moved and king can't be in check
                                    if rook.moveCounter == 0 and self not in piece.legal_moves:
                                        self.legal_moves.append("71")
                                        self.castling = True
                            except IndexError:
                                pass
                        #queenside
                        for f in ["41", "31", "21"]:
                            try:
                                for piece in [k for k in self.pieces if k.colour != self.colour]:
                                    if f in piece.legal_moves and f != "21":
                                        raise StopIteration() #king cannot pass through check while castling
                                    if self.dct1[self.board[f].text] != "": #no pieces can be in between king and rook
                                        raise StopIteration() #StopIteration exception is used here to break out of a
                            except StopIteration:                                          #double (nested) for-loop
                                break

                        else:
                            try:
                                rook = [h for h in self.pieces if h.colour == self.colour and type(h).__name__ is \
                                        "Rook" and h.position == "11"][0] #finding a rook with which to castle
                                for piece in [t for t in self.pieces if t.colour != self.colour]:
                                    #rook can't have moved and king can't be in check
                                    if rook.moveCounter == 0 and self not in piece.legal_moves:
                                        self.legal_moves.append("31")
                                        self.castling = True
                            except IndexError:
                                pass

                    elif self.colour == "B": #castling takes place on 8th rank (black castles)
                        #kingside
                        for f in ["68", "78"]:
                            try:
                                for piece in [k for k in self.pieces if k.colour != self.colour]:
                                    if f in piece.legal_moves:
                                        raise StopIteration() #king cannot pass through check while castling
                                    if self.dct1[self.board[f].text] != "": #no pieces can be in between king and rook
                                        raise StopIteration() #StopIteration exception is used here to break out of a
                            except StopIteration:                                          #double (nested) for-loop
                                break

                        else:
                            try:
                                rook = [h for h in self.pieces if h.colour == self.colour and type(h).__name__ is \
                                        "Rook" and h.position == "88"][0] #finding a rook with which to castle
                                for piece in [t for t in self.pieces if t.colour != self.colour]:
                                    #rook can't have moved and king can't be in check
                                    if rook.moveCounter == 0 and self not in piece.legal_moves:
                                        self.legal_moves.append("78")
                                        self.castling = True
                            except IndexError:
                                pass
                        #queenside
                        for f in ["48", "38", "28"]:
                            try:
                                for piece in [k for k in self.pieces if k.colour != self.colour]:
                                    if f in piece.legal_moves and f != "28":
                                        raise StopIteration() #king cannot pass through check while castling
                                    if self.dct1[self.board[f].text] != "": #no pieces can be in between king and rook
                                        raise StopIteration() #StopIteration exception is used here to break out of a
                            except StopIteration:                                          #double (nested) for-loop
                                break

                        else:
                            try:
                                rook = [h for h in self.pieces if h.colour == self.colour and type(h).__name__ is \
                                        "Rook" and h.position == "18"][0] #finding a rook with which to castle
                                for piece in [t for t in self.pieces if t.colour != self.colour]:
                                    #rook can't have moved and king can't be in check
                                    if rook.moveCounter == 0 and self not in piece.legal_moves:
                                        self.legal_moves.append("38")
                                        self.castling = True
                            except IndexError:
                                pass


    def illegalMoves(self): #checking to see if the king is in check and
        #delegalising moves that put/keep the king under threat
        illegal = [ ] #illegal moves
        for y in self.legal_moves: #iterating over piece's legal moves
            #saving current board positions
            tempOrigin = self.board[self.position].text
            tempDest = self.board[y].text
            self.board[self.position]["text"] = ""  #removing the piece from its old square
            self.board[self.position].text = ""
            self.board[y]["text"] = tempOrigin  #placing the piece at the new position
            self.board[y].text = tempOrigin

            if (self.colour == "W" and self.wKing.check() is True) or \
               (self.colour == "B" and self.bKing.check() is True): #checks if the player's king is in check
                if self.colour == "W": #keeps track of checking piece; piece that is threatening king
                    checking = self.wKing.underThreat(True)
                else: #keeps track of checking piece; piece that is threatening king
                    checking = self.bKing.underThreat(True)

                if type(self).__name__ is not "King":
                    for p in [x for x in self.pieces if x.colour != self.colour]: #iterates over enemy pieces
                        #piece is absolutely pinned; i.e.pinned to king
                        #so can't be moved without exposing the king to a check
                        try:
                            if y == checking.position: #checking piece can be captured
                                if self.position in p.legal_moves:
                                    illegal.append(y) #illegal move
                                raise StopIteration() #StopIteration exception is used here to
                                #break out of a double (nested) for-loop
                        except StopIteration:
                            break
                    else:
                        self.board[self.position]["text"] = tempDest
                        self.board[self.position].text = tempDest
                        illegal.append(y) #illegal move

            if type(self).__name__ is "King":
                for p in [x for x in self.pieces if x.colour != self.colour]:
                    if y in p.legal_moves: #king can only capture checking piece if it is unprotected
                        illegal.append(y) #illegal move
            #replacing pieces that were moved temporarily
            self.board[y]["text"] = tempDest
            self.board[y].text = tempDest
            self.board[self.position]["text"] = tempOrigin
            self.board[self.position].text = tempOrigin

        for k in set(illegal): #removing illegal moves from the list of legal moves
            self.legal_moves.remove(k)

    def getTurn(self): #checks whose turn it is; white or black
        return game.turn[0] == self.colour


    def resetBoard(self): #resets the board to neutral position - no pieces selected
        for j in self.board:
            self.board[j]["command"] = "" #resetting button commands
        for k in self.pieces:
            if k != self:
                self.board[k.position]["command"] = k.showLegalMoves
        for i in self.board: #resetting board colour; every alternate square has a different colour
            if (int(i[0]) + int(i[1])) % 2 == 0:
               self.board[i]["bg"] = "tan4"
            else:
                self.board[i]["bg"] = "ivory2"

    def showLegalMoves(self): #displays the legal moves of a piece when that piece is clicked
        for piece in [x for x in self.pieces if x.colour == self.colour]: #iterates over all pieces of the colour of
            #the player whose turn it is
            piece.legalMoves() #generating a list of all possible legal moves
            piece.illegalMoves() #and removing illegal moves

        if any(self.board[a]["bg"] == "blue" for a in self.board):
            self.resetBoard() #resets board colour if a piece is selected and deselects that piece

        if self.getTurn() is True: #current player's turn
            for c in self.legal_moves: #displays legal moves
                self.board[c]["bg"] = "blue" #by highlighting them blue
                #each legal move button has a command to move the piece to that square
                self.board[c]["command"] = lambda c=c: self.move(c)

    def move(self, newPos): #moves current piece to the required position
        capt = False #not capturing
        self.currentMove = ""
        #removes piece from current location
        self.board[self.position]["text"] = ""
        self.board[self.position].text = ""
        self.board[self.position]["command"] = False
        #destination square is not empty
        if self.dct1[self.board[newPos].text] != "":
            self.capturePiece(newPos) #captures the opponent piece at that square
            capt = True #capturing
        #en-passant
        if type(self).__name__ is "Pawn" and self.enPassant is True: #capturing by en-passant - the only case where
            #a piece does not capture an opponent's piece on the destination square
            if self.colour == "B" and self.dct1[self.board[str(newPos[0])+str(int(newPos[1])+1)].text] == "wP":
                self.capturePiece(str(newPos[0])+str(int(newPos[1])+1))
                capt = True
            if self.colour == "W" and self.dct1[self.board[str(newPos[0])+str(int(newPos[1])-1)].text] == "bP":
                self.capturePiece(str(newPos[0])+str(int(newPos[1])-1))
                capt = True

        self.resetBoard() #resets the board

        if type(self).__name__ is "King": #castling is a king move
            try:
                if self.castling is True: #castling is permitted
                    if math.fabs(int(newPos[0]) - int(self.position[0])) > 1: #king is moving more than one square
                        if self.colour == "W":
                            if newPos == "31": #king goes to c1, rook goes to d1; queenside
                                pos = "11"
                                dest = "41"
                                self.castling = (True, "L") #castling "long", i.e. queenside
                            elif newPos == "71":  #king goes to g1, rook goes to f1; kingside
                                pos = "81"
                                dest = "61"
                                self.castling = (True, "S") #castling "short", i.e. kingside
                        elif self.colour == "B":
                            if newPos == "38": #king goes to c8, rook goes to d8; queenside
                                pos = "18"
                                dest = "48"
                                self.castling = (True, "L") #castling "long", i.e. queenside
                            elif newPos == "78": #king goes to g8, rook goes to f8; kingside
                                pos = "88"
                                dest = "68"
                                self.castling = (True, "S") #castling "short", i.e. kingside
                        #finding the rook with which to castle
                        rook = [x for x in self.pieces if x.colour == self.colour and x.position == pos][0]
                        self.board[pos]["text"] = "" #removing rook from its current location
                        self.board[pos].text = ""
                        self.board[pos]["command"] = False
                        rook.placePiece(dest) #placing the rook at its new location
            except TypeError:
                pass

        if type(self).__name__ is "Pawn":
            if capt is True:
                self.currentMove += self.rank_file[int(self.position[0])] #keeping track of moves in standard notation
            else:
                pass
        elif type(self).__name__ == "Knight":
            self.currentMove += "N" #keeping track of moves in standard notation, N prefixed for knight
        else: #keeping track of moves in standard notation, first letter of piece prefixed
            self.currentMove += type(self).__name__[0]
        if capt is True:
            self.currentMove += "x" #keeping track of moves in standard notation, x denotes capture
        self.currentMove += self.rank_file[int(newPos[0])] #keeping track of moves in standard notation, file of new pos
        self.currentMove += newPos[1] #keeping track of moves in standard notation, rank of new pos
        if type(self).__name__ is "Pawn":
            if self.enPassant is True:
                self.currentMove += "e.p." #keeping track of moves in standard notation, e.p. denotes en-passant capture
            self.enPassant = False
        #check to see if castling has occured
        if type(self).__name__ is "King":
            try:
                if self.castling is not False:
                    #keeping track of moves, O-O/O-O-O denotes kingside/queenside castling respectivly
                    if self.castling[1] == "L": #castling queenside
                        self.currentMove = "O-O-O"
                    elif self.castling[1] == "S": #castling kingside
                        self.currentMove = "O-O"
                    self.castling = False
            except TypeError:
                pass
        #checking to see if a pawn can be promoted
        if type(self).__name__ is "Pawn":
            #pawn has reached the other end of the board
            if self.colour == "W" and newPos[1] == "8":
                self.promote() #pawn can be promoted, i.e. traded for a more valuable piece (K/B/R/Q)
            elif self.colour == "B" and newPos[1] == "1":
                self.promote() #pawn can be promoted, i.e. traded for a more valuable piece (K/B/R/Q)

        #place the piece being moved at its new position
        self.placePiece(newPos)
        self.moveCounter += 1

        #checking to see if the game has ended
        if self.colour == "W":
            if self.bKing.underThreat() is True: #black is in check
                checkMate = self.bKing.checkmate(self) #boolean to test for checkmate
                if checkMate is False:
                    self.bKing.check(self) #boolean to test for check
                else:
                    winner = game.turn[0] #game ends in checkmate - white has won
                    self.board[self.bKing.position]["bg"] = "firebrick4" 
            else:
                if self.bKing.stalemate() is True: #test for stalemate
                    print("1/2-1/2", end="")
                    game.endGame("SM") #game ends by stalemate
        else:
            if self.wKing.underThreat() is True: #white is in check
                checkMate = self.wKing.checkmate(self) #boolean to test for checkmate
                if checkMate is False:
                    self.wKing.check(self) #boolean to test for check
                else:
                    winner = game.turn[0] #game ends in checkmate - black has won
                    self.board[self.wKing.position]["bg"] = "firebrick4" 
            else:
                if self.wKing.stalemate() is True: #test for stalemate
                    print("1/2-1/2", end = "")
                    game.endGame("SM") #game ends by stalemate

        self.moves.append(self.currentMove) #keeps track of moves

        try:
            for i in self.moves[-100:]: #checking for draw by 50 move rule
                if str(i[0]).islower() or "x" in str(i):
                    break  #a pawn has moved or a capture has taken place
                    #within the last 50 moves
            else:  #game drawn by 50 move rule
                game.endGame("50")
        except IndexError: #game is less than 50 moves long
            pass

       #mapping the move number to piece moved
       #and outputting previous move
        if game.turn[0] == "W":
            sys.stdout.write("%i. %s " % ((len(self.moves)/2), self.moves[-1]))
            sys.stdout.flush()
        else:
            sys.stdout.write("%s " % (self.moves[-1]))
            sys.stdout.flush()
        try:
            if winner == "W": #white wins by checkmate
                self.moves.append("1-0")
                print(self.moves[-1])
                game.endGame("CM", winner)
            elif winner == "B": #black wins by checkmate
                self.moves.append("0-1")
                print(self.moves[-1])
                game.endGame("CM", winner)
        except NameError:
            pass

        winsound.PlaySound("chess_piece_sound", winsound.SND_FILENAME) #play sound of piece being placed

        for obj in self.pieces: #iterating over all pieces
            for i in self.board:
                if obj.position == i: #assigning each square that a piece can move to a command to move the piece
                    self.board[i]["command"] = obj.showLegalMoves #to that square

        game.turn.reverse() #other player's turn

        if playAI.get() is True and playerColour.get()!=game.turn[0]:
            ai.randMove(Pieces.pieces, game.turn[0])
        if game.turn[0] == "W": #so that the player looks at the board from their colour's perspective
            game.btn1.config(text="White to play", bg="linen", fg="black")

            if boardFlip.get() is True:  #flips the board every move (if enabled)
                game.switchSides(False)
        else:
            game.btn1.config(text="Black to play", bg="black", fg="linen")
            if boardFlip.get() is True:  #flips the board every move (if enabled)
                game.switchSides(True)

    def underThreat(self, getCheckingPiece=False): #function to check if a piece is under threat
        #(i.e. being attacked) by an opponent piece
        for piece in [x for x in self.pieces if x.colour != self.colour]: #iterates over the list of enemy pieces;
            #a piece can't be threatened by its own coloured pieces
            piece.legalMoves() #generates a list of legal moves for each piece
            if self.position in piece.legal_moves: #to check if the current piece's location is within those legal moves
                self.board[piece.position]["bg"] = "red"
                if getCheckingPiece is True:
                    return piece #returns the piece checking the king
                else:
                    return True #piece is under threat
        self.resetBoard()
        return False #piece is not under threat

    def capturePiece(self, newPos): #captures an opponent's piece when the player's piece lands on the same square
        capt = False
        for piece in self.pieces[:]: #iterating over piece
            if piece.position == newPos: #a piece occupies the new square
                capt = True
                self.captured.append(piece) #capture opponent piece
                self.pieces.remove(piece) #remove piece from list of active pieces
                try:
                    if type(self).__name__ is not "Pawn" or \
                            (type(self).__name__ is "Pawn" and self.enPassant is False):
                        filename=self.board[newPos].text #piece name
                        self.captured_icons.append(filename)
                except (AttributeError, IndexError):
                    pass
                break
            if type(self).__name__ is "Pawn":
                if self.enPassant is True:
                    if self.colour == "B" and self.dct1[self.board[newPos].text] == "wP":
                        capt = True
                        self.captured.append(piece) #capture opponent piece
                        self.pieces.remove(piece) #remove piece from list of active pieces
                        self.board[newPos]["text"] = ""
                        self.board[newPos].text = ""
                        self.board[newPos]["command"] = False
                        filename = self.dct2["wP"] #piece name
                        self.captured_icons.append(filename)
                    elif self.colour == "W" and self.dct1[self.board[newPos].text] == "bP":
                        capt = True
                        self.captured.append(piece) #capture opponent piece
                        self.pieces.remove(piece) #remove piece from list of active pieces
                        self.board[newPos]["text"] = ""
                        self.board[newPos].text = ""
                        self.board[newPos]["command"] = False
                        filename = self.dct2["bP"] #piece name
                        self.captured_icons.append(filename)
        if capt == True:
            #sorting captured pieces by value and colour
            lst1 = [x for x in self.captured_icons if x in ["♕", "♖", "♗", "♘", "♙"]]
            lst2 = [y for y in self.captured_icons if y in ["♛", "♜", "♝", "♞", "♟"]]
            lst3 = ["♕", "♖", "♗", "♘", "♙"]
            lst4 = ["♛", "♜", "♝", "♞", "♟"]

            lst1.sort(key=lambda x: lst3.index(x))
            lst2.sort(key=lambda y: lst4.index(y))
            self.captured_icons=lst1[::-1]+lst2
            #displaying all captured pieces, sorted by colour and value
            game.captured_widget.config(state=NORMAL)
            game.captured_widget.delete(1.0, END)
            for i in self.captured_icons:
                game.captured_widget.insert(END, i+"\n")
            game.captured_widget.config(state=DISABLED)
        #checking for draw by insufficient material
        for piece in self.pieces:
            if type(piece).__name__ is "Pawn" or type(piece).__name__ is "Queen" or \
                type(piece).__name__ is "Rook" or type(piece).__name__ is "Bishop":
                break #Pawn/Rook/2 Bishops/Queen is sufficient material to win
        else:
            game.endGame("IM")  #insufficient material (pieces) for the game to end by checkmate
        bishopsW = [t for t in self.pieces if type(t).__name__ is "Bishop" and t.colour == "W"]
        bishopsB = [t for t in self.pieces if type(t).__name__ is "Bishop" and t.colour == "B"]
        bPieces = [f for f in self.pieces if f.colour == "B"]
        wPieces = [g for g in self.pieces if g.colour == "W"]
        try:
            if (len(bishopsW) == len(wPieces) - 1) or (len(bishopsB) == len(bPieces) - 1):
                if len(bishopsW) == 2 or len(bishopsB) == 2:
                    #bishops are on the same colour; insufficient material
                    if (int(bishopsW[0].position[0])*int(bishopsW[0].position[1])) % 2 == \
                            (int(bishopsW[1].position[0])*int(bishopsW[1].position[1])) % 2:
                        game.endGame("IM")
                    if (int(bishopsB[0].position[0])*int(bishopsB[0].position[1])) % 2 == \
                            (int(bishopsB[1].position[0])*int(bishopsB[1].position[1])) % 2:
                        game.endGame("IM")
                elif len(bishopsW) == 1 or len(bishopsB) == 1:
                    game.endGame("IM")
        except IndexError:
            pass

    def placePiece(self, position): #places piece in required location on board
        self.position = position #current position set to new position
        #checks which child class runs this method so the appropriate piece can be placed
        if type(self).__name__ is "Pawn": #placing a pawn
            if self.colour == "B":
                self.board[self.position]["text"] = self.BP
                self.board[self.position].text = self.BP
            elif self.colour == "W":
                self.board[self.position]["text"] = self.WP
                self.board[self.position].text = self.WP
        elif type(self).__name__ is "Bishop": #placing a bishop
            if self.colour == "B":
                self.board[self.position]["text"] = self.BB
                self.board[self.position].text = self.BB
            elif self.colour == "W":
                self.board[self.position]["text"] = self.WB
                self.board[self.position].text = self.WB
        elif type(self).__name__ is "Knight": #placing a knight
            if self.colour == "B":
                self.board[self.position]["text"] = self.BN
                self.board[self.position].text = self.BN
            elif self.colour == "W":
                self.board[self.position]["text"] = self.WN
                self.board[self.position].text = self.WN
        elif type(self).__name__ is "Rook": #placing a rook
            if self.colour == "B":
                self.board[self.position]["text"] = self.BR
                self.board[self.position].text = self.BR
            elif self.colour == "W":
                self.board[self.position]["text"] = self.WR
                self.board[self.position].text = self.WR
        elif type(self).__name__ is "Queen": #placing a queen
            if self.colour == "B":
                self.board[self.position]["text"] = self.BQ
                self.board[self.position].text = self.BQ
            elif self.colour == "W":
                self.board[self.position]["text"] = self.WQ
                self.board[self.position].text = self.WQ
        elif type(self).__name__ is "King": #placing a king
            if self.colour == "B":
                self.board[self.position]["text"] = self.BK
                self.board[self.position].text = self.BK
            elif self.colour == "W":
                self.board[self.position]["text"] = self.WK
                self.board[self.position].text = self.WK

class King(Pieces): #king class - both kings are instances

    def __init__(self, root, frame, grid, colour, board): #inherits from parent class (Pieces)
         super().__init__(root, frame, grid, colour, board)

    def check(self, activePiece=None): #evaluates whether the king is in check
        #activePiece is the piece that has just been moved
        if self.underThreat() is True and activePiece is not None:
            activePiece.currentMove += "+" #+ indicates a check in standard move notation
            return True
        else:
            return self.underThreat() #returns whether the king is under threat from an enemy piece

    def checkmate(self, activePiece): #evaluates whether the king has been checkmated
        for piece in [x for x in self.pieces if x.colour == self.colour]: #iterates over friendly pieces
            piece.legalMoves()
            piece.illegalMoves()
            if len(piece.legal_moves) == 0: #piece has no legal moves
                continue
            else: #player has at least one legal move (any piece) so not checkmate
                return False
        activePiece.currentMove += "#" #player is checkmated
        return True

    def stalemate(self): #evaluates whether the player has been stalemated
        for piece in [x for x in self.pieces if x.colour == self.colour]: #iterates over friendly pieces
            piece.legalMoves()
            piece.illegalMoves()
            if len(piece.legal_moves) == 0: #piece has no legal moves
                continue
            else:  #player has at least one legal move (any piece) so not stalemate
                return False
        return True #player is stalemated


class Queen(Pieces): #queen class - all queens are instances

    def __init__(self, root, frame, grid, colour, board): #inherits from parent class (Pieces)
         super().__init__(root, frame, grid, colour, board)


class Rook(Pieces): #queen rooks - all rooks are instances

    def __init__(self, root, frame, grid, colour, board): #inherits from parent class (Pieces)
         super().__init__(root, frame, grid, colour, board)


class Knight(Pieces): #knight class - all knights are instances

    def __init__(self, root, frame, grid, colour, board): #inherits from parent class (Pieces)
         super().__init__(root, frame, grid, colour, board)


class Bishop(Pieces): #bishop class - all bishops are instances

    def __init__(self, root, frame, grid, colour, board): #inherits from parent class (Pieces)
         super().__init__(root, frame, grid, colour, board)


class Pawn(Pieces): #pawn class - all pawns are instances

    def __init__(self, root, frame, grid, colour, board): #inherits from parent class (Pieces)
         super().__init__(root, frame, grid, colour, board)

    def promote(self): #a pawn must promote to a more valuable piece (Q/R/B/N) when it reaches the player's last rank;
        #8th rank for white, 1st rank for black
        promoteChoice = Toplevel() #toplevel widget to allow user to pick promotion choice
        promoteChoice.geometry("150x150")
        promoteChoice.resizable(0,0)
        promoteChoice.attributes("-topmost", True)
        self.promoteVar = StringVar() #keeps track of promotion choice
        self.promoteVar.set(None)

        for i in ["Queen", "Rook", "Bishop", "Knight"]:
            r = Radiobutton(promoteChoice, text = i, variable = self.promoteVar, value = i)
            r.pack(anchor = W)
        promoteChoice.focus_force()

        while True: #forces the user to pick a promotion or cancel move
            #since promotion is not optional (a pawn cannot stay on the player's last rank)
            if self.promoteVar.get() == "Queen": #promotion to queen
                self.__class__ = Queen #changing the instance's (current pawn) class to queen; pawn becomes queen
                self.currentMove += "Q" #move notation for promotion to queen (queening)
                promoteChoice.destroy()
                break
            elif self.promoteVar.get() == "Knight": #promotion to knight
                self.__class__ = Knight #changing the instance's (current pawn) class to knight; pawn becomes knight
                self.currentMove += "N" #move notation for promotion to knight
                promoteChoice.destroy()
                break
            elif self.promoteVar.get() == "Rook": #promotion to rook
                self.__class__ = Rook #changing the instance's (current pawn) class to rook; pawn becomes rook
                self.currentMove += "R" #move notation for promotion to rook
                promoteChoice.destroy()
                break
            elif self.promoteVar.get() == "Bishop": #promotion to bishop
                self.__class__ = Bishop #changing the instance's (current pawn) class to bishop; pawn becomes bishop
                self.currentMove += "B" #move notation for promotion to bishop
                promoteChoice.destroy()
                break
            else:
                self.root.update()
                continue


#class for the game itself
class Chess:

    def __init__(self, root):
        self.root = root #main GUI window
        #creating a data structure to keep track of the board
        self.alph = list("abcdefgh")
        self.board = [str(j)+str(i) for i in range(1, 9) for j in range(1, 9)] #variables to keep track of the
        #chess board using coordinates, e.g. a1, c2, f7 or g3
        self.grid = [ ] #keeps track of grid squares (emulated by Tkinter buttons)
        self.turn = ["W", "B"] #keeps track of whose turn it is by reversing every move

    def createBoard(self): #making a board
        #setting up GUI frames
        self.frame1 = Frame(self.root, height=600, width=600) #game frame
        self.frame1.grid(sticky=N+S, row=2, column=4, padx=(50, 100), pady=75)

        self.frame2 = Frame(self.root, height=600, width=100) #left sidebar frame
        self.frame2.grid(sticky=W, row=2, rowspan=5, column=3, padx=(0, 0), pady=10, ipadx=10, ipady=10)

        self.frame3 = Frame(self.root, height=200, width=600) #bottom (horizontal) sidebar
        self.frame3.grid(sticky=N+S, row=3, column=4)
        #making the frames expand evenly
        self.frame1.grid_propagate(False)
        self.frame2.grid_propagate(False)
        self.frame3.grid_propagate(False)
        #widget to display captured pieces
        self.captured_widget = Text(self.frame2, font=("Segoe UI Symbol", "32"), \
                                    relief="flat", bg="#f0f0ed", state=DISABLED)
        self.captured_widget.grid()
        self.captured_widget.config(state=NORMAL)
        self.captured_widget.config(state=DISABLED)
        for i in range(100):
            self.frame2.rowconfigure(i, weight=1)
            self.frame2.grid_rowconfigure(i, weight=1)
        #auto expand grid squares
        for i in range(1, 9):
            self.root.rowconfigure(i, weight=1)
            self.root.columnconfigure(i, weight=1)
            self.root.grid_propagate(False)
            Grid.columnconfigure(self.frame1, i, weight=1)
            Grid.rowconfigure(self.frame1, i, weight=1)
        #initialising variables
        grid_size = 8
        grid_counter = grid_size ** 2
        row = 1
        #each grid square on the chess board is a button with a relevant command for moving pieces
        #creating buttons to fill the grid, as many as necessary, depending on grid size, in this case 8x8
        for i in range(grid_counter, 0, -1):
            column = i % grid_size #calculating the column in which to put the button
            if column == 0:
                column = grid_size
            if i % grid_size == 0 and i != (grid_size ** 2): #calculating the row in which to put the button
                row += 1
            #creating checkerboard squares using buttons, squares alternate colours so no two
            #adjacent squares have the same colour
            if (column + row) % 2 == 0: #light squares
               gridSq = Button(self.frame1, height=3, width=7, bg = "ivory2", text = "", activebackground = "ivory2", \
                               compound = "c", borderwidth = 1, font=("Segoe UI Symbol", "32"), \
                               relief = "ridge", overrelief = "sunken")
            else: #dark squares
                gridSq = Button(self.frame1, bg = "tan4", text = "", activebackground = "tan4", \
                                compound = "c", borderwidth = 1, font=("Segoe UI Symbol", "32"), \
                                relief = "ridge", overrelief = "sunken")
            gridSq.grid(row=row, column=column, sticky=N+S+E+W) #positioning grid squares
            gridSq.text = "" #squares start off empty; pieces will be added later
            self.grid.append(gridSq) #adding the square locations to a list
        #bottom sidebar GUI widgets/elements: flip board button, turn indicator, export moves button, resign button
        self.btn1 = Label(self.frame3, text = "White to play", bg="linen", fg="black", font="Verdana 14")
        self.btn1.grid(row=2, column=2, sticky=W, pady=10)

        self.btn2 = Button(self.frame3, text="Switch board orientation", bd=0, font="Verdana 12", \
                           command=lambda: self.switchSides(True))
        self.btn2.grid(row=2, column=1, sticky=W, pady=10)

        self.btn3 = Button(self.frame3, text="Export moves", bd=0, font="Verdana 12", command=lambda: self.getMoves())
        self.btn3.grid(row=2, column=3, sticky=E, pady=10)

        self.btn4 = Button(self.frame3, text="Resign", bd=0, font="Verdana 12", \
                           command=lambda: game.endGame("R", game.turn[1]))
        self.btn4.grid(row=2, column=4, sticky=E, pady=10)
        #creating a mapped connection between coordinates and grid square
        self.boardMap = dict(zip(self.board, self.grid[::-1]))

    def getMoves(self):
        moves=Toplevel() #outputs the moves played to the user, these moves can then be copied and analysed elsewhere
        moves.attributes("-topmost", True) #creates and displays a window to show moves
        lbl = Text(moves) #text widget to show moves
        lbl.pack()
        for i in range(len(Pieces.moves)): #iterating over previous moves
            if i % 2 != 0: #white's move; prefaced by move number
                try:
                    if "#" not in Pieces.moves[i-1]:
                        lbl.insert(END, "%i. %s " % ((i+2)/2, Pieces.moves[i])) #output move
                    else:
                        lbl.insert(END, "%s " % (Pieces.moves[i])) #output move
                except IndexError:  pass
            else: #black's move
                lbl.insert(END, ("%s " % (Pieces.moves[i]))) #output move

    def switchSides(self, white_down):
        #switching board orientation
        grid_size = 8
        grid_counter = grid_size ** 2
        row = 1
        #creating enough labels to fill the grid, as many as necessary, depending on grid size
        for i in range(grid_counter, 0, -1):
            column = i % grid_size #calculating the column in which to put the label
            if column == 0:
                column = grid_size
            if i % grid_size == 0 and i != (grid_size ** 2): #calculating the row in which to put the label
                row += 1

            if white_down is True:
                self.grid[i-1].grid(row = row, column = column, sticky=N+S+E+W) #positioning grid squares
                self.btn2.config(command = lambda: self.switchSides(False))
            else:
                self.grid[64-i].grid(row = row, column = column, sticky=N+S+E+W) #positioning grid squares
                self.btn2.config(command = lambda: self.switchSides(True))

    def createPieces(self): #creates all the chess pieces and placing them at their starting positions on the board
        #creating:
        for i in range(8): #8 white pawns
            exec("self.pW%s=Pawn(self.root, self.frame1, self.grid, 'W', self.boardMap)" % (i+1))
            exec("self.pW%s.placePiece('%s')" % (i+1,str(i+1)+str(2)))
        for i in range(8): #8 black pawns
            exec("self.pB%s=Pawn(self.root, self.frame1, self.grid, 'B', self.boardMap)" % (i+1))
            exec("self.pB%s.placePiece('%s')" % (i+1, str(i+1)+str(7)))
        for i in range(0, 4, 3): #2 white bishops
            exec("self.bW%s=Bishop(self.root, self.frame1, self.grid, 'W', self.boardMap)" % (int(i/2)+1))
            exec("self.bW%s.placePiece('%s')" % (int(i/2)+1, str(i+3)+str(1)))
        for i in range(0, 4, 3): #2 black bishops
            exec("self.bB%s=Bishop(self.root, self.frame1, self.grid, 'B', self.boardMap)" % (int(i/2)+1))
            exec("self.bB%s.placePiece('%s')" % (int(i/2)+1, str(i+3)+str(8)))
        for i in range(0, 6, 5): #2 white knights
            exec("self.nW%s=Knight(self.root, self.frame1, self.grid, 'W', self.boardMap)" % (int(i/5)+1))
            exec("self.nW%s.placePiece('%s')" % (int(i/5)+1, str(i+2)+str(1)))
        for i in range(0, 6, 5): #2 black knights
            exec("self.nB%s=Knight(self.root, self.frame1, self.grid, 'B', self.boardMap)" % (int(i/5)+1))
            exec("self.nB%s.placePiece('%s')" % (int(i/5)+1, str(i+2)+str(8)))
        for i in range(0, 8, 7): #2 white rooks
            exec("self.rW%s=Rook(self.root, self.frame1, self.grid, 'W', self.boardMap)" % (int(i/7)+1))
            exec("self.rW%s.placePiece('%s')" % (int(i/7)+1,  str(i+1)+str(1)))
        for i in range(0, 8, 7): #2 black rooks
            exec("self.rB%s=Rook(self.root, self.frame1, self.grid, 'B', self.boardMap)" % (int(i/7)+1))
            exec("self.rB%s.placePiece('%s')" % (int(i/7)+1, str(i+1)+str(8)))
        #a white queen
        exec("self.qW%s=Queen(self.root, self.frame1, self.grid, 'W', self.boardMap)" % (1))
        exec("self.qW%s.placePiece('%s')" % (1, "41")) #d1
        #a black queen
        exec("self.qB%s=Queen(self.root, self.frame1, self.grid, 'B', self.boardMap)" % (1))
        exec("self.qB%s.placePiece('%s')" % (1, "48")) #d8
        #a white king
        self.kW=King(self.root, self.frame1, self.grid, 'W', self.boardMap)
        self.kW.placePiece("51") #e1
        #a black king
        self.kB=King(self.root, self.frame1, self.grid, 'B', self.boardMap)
        self.kB.placePiece("58") #e8

    def displayLegalMoves(self, x): #returns the command to show the legal moves for the piece at that square
        return x.showLegalMoves

    def startGame(self):
        for obj in gc.get_objects(): #iterating over instances of objects
            for x in self.boardMap: #iterating over locations on the board
                if isinstance(obj, Pieces): #object is a piece
                    buttonCommand = self.displayLegalMoves(obj)
                    if obj.position == x: #piece is at position x
                        self.boardMap[x]["command"] = buttonCommand #clicking on the piece at position x will display
                        #the piece's legal moves
        if playAI.get() is True and playerColour.get() != game.turn[0]:
            ai.randMove(Pieces.pieces, game.turn[0])


    def endGame(self, case, winner=None):
        #game ends by checkmate
        if case == "CM" and winner == "W":
            messagebox.showinfo("Checkmate", "White wins by checkmate!")
        elif case == "CM" and winner == "B":
            messagebox.showinfo("Checkmate", "Black wins by checkmate!")
        #game ends by resignation
        elif case == "R" and winner == "W":
            messagebox.showinfo("Black resigns", "White wins by resignation!")
        elif case == "R" and winner == "B":
            messagebox.showinfo("White resigns", "Black wins by resignation!")
        #game ends by stalemate
        elif case == "SM":
            messagebox.showinfo("Stalemate", "Draw by stalemate")
        #game ends by draw by agreement
        elif case == "D":
            messagebox.showinfo("Draw", "Draw by agreement")
        #game ends by insufficient material
        elif case == "IM":
            messagebox.showinfo("Draw", "Draw by insufficient material")
        #game ends by the same position occurring three times
        elif case == "3R":
            messagebox.showinfo("Draw", "Draw by threefold repetition")
        #game ends by the lapse of fifty moves with no pawn movement or capture
        elif case == "50":
            messagebox.showinfo("Draw", "Draw by fifty-move rule")
        for sq in self.boardMap:
            self.boardMap[sq].config(command=False)
        self.root.destroy()
        menu()

#setting up the GUI
def menu():
    global master, root, boardFlip, playAI, playerColour
    master=Tk()
    master.title("Chess")
    master.resizable(0,0)
    master.iconbitmap(default = "chess.ico")
    master.attributes("-topmost", True)
    master.geometry("325x350")
    root = Toplevel(master)
    root.resizable(0,0)
    root.attributes("-topmost", True)
    root.geometry("725x675")
    root.withdraw()
    boardFlip = BooleanVar(master, value=False)
    playAI = BooleanVar(master, value=True)
    playerColour = StringVar(master, value="W")
    lbl = Label(master, text="Chess", font=("MS Serif", "24", "bold"), bg="tan4", fg="ivory2")
    lbl.pack(fill=X)
    btn1 = Button(master, text="Start Game", font="Verdana 18", command=lambda: start(master, root))
    btn1.pack(fill=X)
    btn2 = Checkbutton(master, text="Play against computer", font="Verdana 14", variable=playAI)
    btn2.pack(fill=X)
    lbl2 = Label(master, text="Play as", font="Verdana 12")
    lbl2.pack()
    fr=Frame(master)
    fr.pack()
    btn3 = Radiobutton(fr, text="White", font="Verdana 10", variable=playerColour, value="W")
    btn3.pack(side="left")
    btn4 = Radiobutton(fr, text="Black", font="Verdana 10", variable=playerColour, value="B")
    btn4.pack(side="right")
    bFlip = Checkbutton(master, text="Auto-flip board", font="Verdana 14", variable=boardFlip)
    bFlip.pack(fill=X)
    btn5 = Button(master, text="How to play", font="Verdana 18", bd=0, \
                  command=lambda:webbrowser.open_new("https://www.chess.com/learn-how-to-play-chess"))
    btn5.pack(fill=X, side=BOTTOM)
    btn2.config(command=lambda: enable_disable)
    #block option to play as w/b if there are two players
    def enable_disable():
        btn3.config(state=DISABLED if playAI.get() is False else NORMAL)
        btn4.config(state=DISABLED if playAI.get() is False else NORMAL)

    btn2.config(command=enable_disable)
def start(master, root): #starts the program by creating the GUI windows
    global game
    master.withdraw()
    game = Chess(root)
    game.createBoard()
    game.createPieces()
    game.startGame()
    root.deiconify()


if __name__ == "__main__":
    menu() #creates the menu
    root.bind("<Control-w>", lambda x: root.destroy())
    #overides the window close button - warns user before closing as the game will not be saved
    root.protocol("WM_DELETE_WINDOW", lambda: root.destroy() \
        if messagebox.askokcancel("Chess", """Are you sure you want to quit? \nYour game will not be saved""") \
        else False)
    master.mainloop()