import copy
from settings import settings


class TetrisPieceInterface:
    # 0 = not_taken, 1 = taken
    # all_taken_positions = [[0]*16] * 16
    # colors = ["Red", "Green", "Blue", "Yellow"]
    colors = ["#cc0066","#00cc99","#0033cc","#ffcc00"]
    color_index = 0
    all_taken_positions = [[0 for i in range(16)] for i in range(16)]
    def __init__(self,row:int,column:int, form = 0):
        self.position = [[row,column],
                    [row , column],
                    [row, column],
                    [row,column]]
        self.form = form
        self.color = TetrisPieceInterface.colors[TetrisPieceInterface.color_index]
        TetrisPieceInterface.color_index = (TetrisPieceInterface.color_index + 1) % 4
        self.build([row,column],form)
    
    def build(self, build_around):
        pass

    def can_it_move(self,dir="Down"):
        new_poisition = []
        
        if(dir == "Down"): 
            if(settings.tetris_mode in ["NORMAL", "DOUBLE_TROBLE", "PHANTOM_BLOCKS","FLIP"]): 
                new_poisition = [[row+1,col] for [row,col] in self.position]
            elif(settings.tetris_mode == "GRAVITY_SHIFT"):
                new_poisition = [[row-1,col] for [row,col] in self.position]
        

        elif(dir == "Right"):new_poisition = [[row,col + 1] for [row,col] in self.position]

        elif(dir == "Left"): new_poisition = [[row,col-1] for [row,col] in self.position]

        return self.valiate_position(new_poisition)

    def move(self, dir="Down"):
        if(self.can_it_move(dir)):

            self.update_taken_place("TAKE")

            if(dir == "Down"):
                if(settings.tetris_mode in ["NORMAL", "DOUBLE_TROBLE", "PHANTOM_BLOCKS","FLIP"]):
                    self.position = [[row + 1, column] for [row,column] in self.position]
                if(settings.tetris_mode == "GRAVITY_SHIFT"):
                    self.position = [[row - 1, column] for [row,column] in self.position]
            elif(dir == "Right"):
                self.position = [[row, column + 1] for [row,column] in self.position]
            else:
                self.position = [[row, column - 1] for [row,column] in self.position]
            self.update_taken_place("PUT")

    def rotate(self):
        row , col = self.position[1][0],self.position[1][1]
        self.build([row,col],(self.form + 1) % 4 )
        self.form = (self.form + 1) % 4 

    def update_taken_place(self,query= "PUT"):

        if (query == "PUT"):

            for [row,col] in self.position:
                TetrisPieceInterface.all_taken_positions[row][col] = 1

        else:

            for [row,col] in self.position:
                TetrisPieceInterface.all_taken_positions[row][col] = 0

    def valiate_position(self, position = []):

        if (not position):
            position = self.position

        for point in position:

            if point[0] not in range(16) or point[1] not in range(16):
                return False

            if point not in self.position and TetrisPieceInterface.all_taken_positions[point[0]][point[1]]:
                return False

        return True

    def kick_and_put_piece(self,new_position):
        kicks = sorted([(i,j) for i in range(-2,2) for j in range(-2,2)], key=lambda kick: abs(kick[0]) + abs(kick[1]))

        for kick in kicks:
            kicked_piece_position = [ [row + kick[0], col + kick[1]] for [row,col] in new_position ]
            if (self.valiate_position(kicked_piece_position)):
                # print(f"from {self.position} to {new_poisition}")
                self.update_taken_place("TAKE")
                self.position = kicked_piece_position
                self.update_taken_place("PUT")
                return

    def ghost_piece(self):
        if(settings.tetris_mode in ["NORMAL", "DOUBLE_TROBLE","FLIP"]):
            lowest_it_can_go = []

            for point in self.position:
                counter = 0
                for i in range(16):
                    if(self.valiate_position([row+i,col] for [row,col] in self.position)):
                        counter = i
                    else:
                        break
                    # if(TetrisPieceInterface.all_taken_positions[point[0]+i][point[1]] == 0):
                        # counter += 1
                    # else:
                        # break
                # if counter < lowest_it_can_go:
                    # lowest_it_can_go = counter
                lowest_it_can_go.append(counter)
        # print([[row+ min(lowest_it_can_go),col] for [row,col] in self.position])
            return [[row+ min(lowest_it_can_go),col] for [row,col] in self.position]
        elif(settings.tetris_mode == "GRAVITY_SHIFT"):
            highest_it_can_go = []

            for point in self.position:
                counter = 0
                for i in range(16):
                    if(self.valiate_position([row-i,col] for [row,col] in self.position)):
                        counter = i
                    else:
                        break
                    # if(TetrisPieceInterface.all_taken_positions[point[0]+i][point[1]] == 0):
                        # counter += 1
                    # else:
                        # break
                # if counter < lowest_it_can_go:
                    # lowest_it_can_go = counter
                highest_it_can_go.append(counter)
        # print([[row+ min(lowest_it_can_go),col] for [row,col] in self.position])
            return [[row-min(highest_it_can_go),col] for [row,col] in self.position]
        elif(settings.tetris_mode == "PHANTOM_BLOCKS" or settings.tetris_mode == "FLIP"):
            return []
    @classmethod
    def check_game_over(cls):
        
        if(sum(TetrisPieceInterface.all_taken_positions[0]) > 0 and settings.tetris_mode== "NORMAL"):
            return True

        if(sum(TetrisPieceInterface.all_taken_positions[15]) > 0 and settings.tetris_mode== "GRAVITY_SHIFT"):
            return True

        return False
    

    @classmethod
    def is_any_row_clear(cls):

        for row in cls.all_taken_positions:
            if(sum(row) == 16):
                return True 

        return False

    @classmethod    
    def clear_full_rows(cls):
        all_cleared_rows_indexes = []
        for row_index in range(len(cls.all_taken_positions)):

            if(sum(cls.all_taken_positions[row_index]) == 16):
                # TetrisPieceInterface.all_taken_positions[row_index]= [0 for i in range(16)]
                copy_positions = copy.deepcopy(cls.all_taken_positions)

                if(settings.tetris_mode in ["NORMAL", "DOUBLE_TROBLE", "PHANTOM_BLOCKS","FLIP"]): 
                    for row_index in range(1,row_index+1):
                        for col_index in range(16):
                            cls.all_taken_positions[row_index][col_index] =  copy_positions[row_index-1][col_index]
                elif(settings.tetris_mode == "GRAVITY_SHIFT"):
                    for row_index in range(row_index,15):
                        for col_index in range(16):
                            cls.all_taken_positions[row_index][col_index] =  copy_positions[row_index+1][col_index]


                all_cleared_rows_indexes.append(row_index)
        return all_cleared_rows_indexes
    
    

    @classmethod
    def back_to_normal(cls):
        if(settings.tetris_mode == "GRAVITY_SHIFT"):
            return cls.undo_gravity_shift()


    @classmethod
    def gravity_shift(cls):
        settings.tetris_mode = "GRAVITY_SHIFT"
        empty_rows = 0
        not_empty_rows = 0
        taken_positions_copy = copy.deepcopy(cls.all_taken_positions)
        for i in range(16):
            if(sum(cls.all_taken_positions[i]) == 0):
                empty_rows +=1 
            else:
                not_empty_rows = 16 - empty_rows
                break

        for i in range(not_empty_rows):
            cls.all_taken_positions[i] = taken_positions_copy[empty_rows + i]
            cls.all_taken_positions[empty_rows + i]= [0 for j in range(16)]

        return empty_rows
    
    @classmethod
    def undo_gravity_shift(cls):
        settings.tetris_mode = "NORMAL"
        empty_rows = 0
        not_empty_rows = 0
        taken_positions_copy = copy.deepcopy(cls.all_taken_positions)
        for i in range(16):
            if(sum(cls.all_taken_positions[i]) != 0):
                not_empty_rows +=1 
            else:
                empty_rows = 16 - not_empty_rows
                break

        for i in range(not_empty_rows):
            cls.all_taken_positions[empty_rows + i] = taken_positions_copy[i]
            cls.all_taken_positions[i]= [0 for j in range(16)]

        return empty_rows
            

class IShapePiece(TetrisPieceInterface):

    def build(self, build_around, form= 0):

        row,column = build_around[0],build_around[1]
        
        if (form % 2 == 0):
            new_position = [[row-1,column],
                            [row, column],
                            [row+1, column],
                            [row+2,column]]

        else:
            new_position = [[row,column-1],
                            [row, column],
                            [row, column+1],
                            [row,column+2]]

        self.kick_and_put_piece(new_position)
            
class JShapePiece(TetrisPieceInterface):
    
    def build(self, build_around, form=0):

        row,column = build_around[0],build_around[1]
        
        if(form == 0):
            new_position = [
                [row-1,column],
                [row,column],
                [row+1,column],
                [row+1,column-1]
            ]
        elif (form == 1):
            new_position = [
                [row,column+1],
                [row,column],
                [row,column-1],
                [row-1,column-1]
            ]
        elif( form == 2):
            new_position = [
                [row-1,column+1],
                [row,column],
                [row-1,column],
                [row+1,column]
            ]
        else:
            new_position = [
                [row,column-1],
                [row,column],
                [row,column+1],
                [row+1,column+1]
            ]

        self.kick_and_put_piece(new_position)

class LShapePiece(TetrisPieceInterface):

    def build(self,build_around,form=0):

        row,column = build_around[0],build_around[1]
        
        if(form == 0):
            new_position = [
                [row-1,column],
                [row,column],
                [row+1,column],
                [row+1,column+1]
            ]
        elif (form == 1):
            new_position = [
                [row,column+1],
                [row,column],
                [row,column-1],
                [row+1,column-1]
            ]
        elif( form == 2):
            new_position = [
                [row-1,column-1],
                [row,column],
                [row-1,column],
                [row+1,column]
            ]
        else:
            new_position = [
                [row,column-1],
                [row,column],
                [row,column+1],
                [row-1,column+1]
            ]

        self.kick_and_put_piece(new_position)

class OShapePiece(TetrisPieceInterface):

    def build(self, build_around, form= 0):

        row,column = build_around[0],build_around[1]

        self.kick_and_put_piece ([
            [row-1,column-1],
            [row,column],
            [row-1,column],
            [row,column-1]
        ])

class SShapePiece(TetrisPieceInterface):

    def build(self, build_around, form= 0):
        row,column = build_around[0],build_around[1]
        
        if(form == 0):
            new_position = [
                [row,column-1],
                [row,column],
                [row-1,column],
                [row-1,column+1]
            ]
        elif (form == 1):
            new_position = [
                [row+1,column],
                [row,column],
                [row,column-1],
                [row-1,column-1]
            ]
        elif( form == 2):
            new_position = [
                [row,column-1],
                [row,column],
                [row-1,column],
                [row-1,column+1]
            ]
        else:
            new_position = [
                [row+1,column],
                [row,column],
                [row,column-1],
                [row-1,column-1]
            ]

        self.kick_and_put_piece(new_position)

class ZShapePiece(TetrisPieceInterface):

    def build(self, build_around, form= 0):
        row,column = build_around[0],build_around[1]
        
        if(form == 0):
            new_position = [
                [row,column-1],
                [row,column],
                [row+1,column],
                [row+1,column+1]
            ]
        elif (form == 1):
            new_position = [
                [row-1,column],
                [row,column],
                [row,column-1],
                [row+1,column-1]
            ]
        elif( form == 2):
            new_position = [
                [row,column-1],
                [row,column],
                [row+1,column],
                [row+1,column+1]
            ]
        else:
            new_position = [
                [row-1,column],
                [row,column],
                [row,column-1],
                [row+1,column-1]
            ]

        self.kick_and_put_piece(new_position)

class TShapePiece(TetrisPieceInterface):

    def build(self, build_around, form= 0):
        row,column = build_around[0],build_around[1]
        
        if(form == 0):
            new_position = [
                [row,column-1],
                [row,column],
                [row,column+1],
                [row+1,column]
            ]
        elif (form == 1):
            new_position = [
                [row-1,column],
                [row,column],
                [row+1,column],
                [row,column-1]
            ]
        elif( form == 2):
            new_position = [
                [row,column-1],
                [row,column],
                [row,column+1],
                [row-1,column]
            ]
        else:
            new_position = [
                [row-1,column],
                [row,column],
                [row+1,column],
                [row,column+1]
            ]

        self.kick_and_put_piece(new_position)

if __name__ == "__main__":
    i = IShapePiece(5,5)
    i.rotate()
    i.move()
    i.move()