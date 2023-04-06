import chocoToken
import sys
sys.path.append('../')
from lib import dictionary as dic

class Scanner:
    def __init__(self) -> None:
        self.cur_char = ""
        self.cur_word = ""
        self.idx_line = 0
        self.idx_char = 0
        self.total_lines = 0
        self.end_doc = False

    def open_file(self, file_name):     #Open the file and counts how many lines has
        self.file=open("../test/"+file_name,"r")
        self.lines = self.file.readlines()
        self.total_lines = len(self.lines)
    
    def getTokens(self):                #Getting all the tokens in the file .txt
        self.token_in_line = False    
        self.update_cur_char()
        while not self.end_doc:         
            cur_token=chocoToken.Token()  # We create token in every iteration

            next_char = self.peek_char()
            if self.cur_char.isalpha():     #Identify if is a keyword or ID
                self.cur_word+=self.cur_char
                while next_char!=False and (next_char.isalpha() or next_char.isdecimal() or next_char == '_'):  #We acumulate the word until there's no alpha character
                    self.get_char()
                    self.cur_word+=self.cur_char 
                    next_char = self.peek_char()
                cur_token.name=self.cur_word
                self.token_in_line = True
                if dic.keywords.get(self.cur_word) != None:     #Verify if it's a Keyword, else ID
                    cur_token.type="KEYWORD"
                else:
                    cur_token.type="ID"
                cur_token.print_token()
            elif self.cur_char.isdecimal():
                self.cur_word+=self.cur_char
                while next_char!=False and next_char.isdecimal():  #We acumulate the word until there's no alpha character
                    self.get_char()
                    self.cur_word+=self.cur_char 
                    next_char = self.peek_char()
                if next_char==' ':
                    cur_token.name=self.cur_word
                    cur_token.type = 'INTEGER'
                    self.token_in_line = True
                    cur_token.print_token()
                #else:
                    #ERROR 
            else:
                self.cur_word+=self.cur_char
                while next_char!= False and ~(next_char.isalpha() or next_char.isdecimal() or next_char == '_') :  #We acumulate the word until there's no alpha character
                    self.get_char()
                    self.cur_word+=self.cur_char 
                    next_char = self.peek_char()
                if dic.operators.get(self.cur_word) != None:
                    cur_token.type = "OPERATOR"
                elif dic.bin_op.get(self.cur_word) != None:
                    cur_token.type = "BIN OPERATOR"

            self.cur_word = ''

            if next_char == False:          #If nextchar is False means it's the end of the txt
                self.end_doc = True
            elif next_char == '#':
                self.get_char()
                self.jump_line()
            else:
                self.get_char()           #We get the next char for the following iterations
    
    def get_char(self):    #Moves the current char to the next char if it exists, otherwise return False
        if self.cur_char != '\n':
            self.idx_char += 1
            self.update_cur_char()
            return True
        else:
            return self.jump_line()
        
    def peek_char(self): #Returns the next char if it exists, otherwise return False
        if self.cur_char != '\n' and self.idx_char+1<len(self.lines[self.idx_line]):
            return self.lines[self.idx_line][self.idx_char+1]
        elif self.total_lines-1 > self.idx_line:
            return self.lines[self.idx_line+1][0]
        else:
            return False

    def jump_line(self): #We jump to the next line, if there was a token in the previous line we create a literal
        jump = False
        if self.total_lines-1 > self.idx_line:
            self.idx_line+=1
            self.idx_char = 0
            self.update_cur_char()
            jump=True
        else:
            self.end_doc = True
        if self.token_in_line:
            literal = chocoToken.Token("NEWLINE","LITERAL")
            literal.print_token()
            self.token_in_line = False
        return jump


    def update_cur_char(self):
        self.cur_char = self.lines[self.idx_line][self.idx_char]


    def __del__(self):
        if self.file != None:
            self.file.close()
        print("Destructor")